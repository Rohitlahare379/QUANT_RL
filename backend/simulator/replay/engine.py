import asyncio
import logging
from typing import AsyncGenerator
from sqlalchemy.orm import Session
from sqlalchemy import asc

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from database import SessionLocal
from market_data.storage.models import MarketCandle
from market_data.normalizers.schemas import NormalizedCandle
from simulator.models.replay import ReplayConfig, ReplayState, ReplayStatus

logger = logging.getLogger("ReplayEngine")

class ReplayEngine:
    """
    Historical Replay Engine that yields normalized market candles sequentially.
    Memory footprint is minimized through paginated database fetching.
    Independent from strategy execution and portfolio management.
    """
    def __init__(self, config: ReplayConfig):
        self.config = config
        self.state = ReplayState(
            status=ReplayStatus.STOPPED,
            current_time=config.start_time
        )
        self._db: Session = SessionLocal()
        
    def start(self):
        """Start or resume the replay."""
        if self.state.status in [ReplayStatus.STOPPED, ReplayStatus.PAUSED]:
            self.state.status = ReplayStatus.PLAYING
            logger.info(f"[ReplayEngine] Replay RESUMED/STARTED. Speed: {self.config.speed_multiplier}x")
            
    def pause(self):
        """Pause the replay session."""
        if self.state.status == ReplayStatus.PLAYING:
            self.state.status = ReplayStatus.PAUSED
            logger.info("[ReplayEngine] Replay PAUSED.")
            
    def stop(self):
        """Stop the replay session completely."""
        self.state.status = ReplayStatus.STOPPED
        logger.info("[ReplayEngine] Replay STOPPED by user.")

    def set_speed(self, multiplier: float):
        """Adjust the replay speed multiplier dynamically."""
        self.config.speed_multiplier = multiplier
        logger.info(f"[ReplayEngine] Speed updated to {multiplier}x")

    async def validate_dataset(self) -> int:
        """
        Check if any candles exist for the current configuration.
        Returns the total count of matching candles.
        """
        count = await asyncio.to_thread(self._get_total_count)
        return count

    def _get_total_count(self) -> int:
        """Synchronously get total candle count for config."""
        return self._db.query(MarketCandle).filter(
            MarketCandle.symbol.in_(self.config.symbols),
            MarketCandle.timeframe == self.config.timeframe,
            MarketCandle.timestamp >= self.config.start_time,
            MarketCandle.timestamp <= self.config.end_time
        ).count()

    async def _handle_speed_and_state(self):
        """Handles replay speed delays and pausing logic."""
        while self.state.status == ReplayStatus.PAUSED:
            await asyncio.sleep(0.1)
            
        if self.state.status == ReplayStatus.STOPPED:
            raise StopAsyncIteration
            
        if self.config.speed_multiplier > 0:
            # Simulate real time passage relative to speed multiplier
            # e.g., 1h timeframe = 3600 real seconds.
            # 3600 / 100x speed = 36 seconds sleep. 
            # Simplified generic delay:
            await asyncio.sleep(1.0 / self.config.speed_multiplier)
        else:
            # Yield to event loop to prevent blocking
            await asyncio.sleep(0)

    async def stream_candles(self) -> AsyncGenerator[NormalizedCandle, None]:
        """
        Incrementally fetch and yield candles chronologically from the database.
        Pagination ensures we don't load massive datasets into memory.
        """
        if self.state.status != ReplayStatus.PLAYING:
            self.start()
            
        batch_size = 1000
        offset = 0
        
        try:
            while self.state.status != ReplayStatus.STOPPED:
                # Run sync DB query in thread pool
                candles = await asyncio.to_thread(
                    self._fetch_candle_batch, batch_size, offset
                )
                
                logger.info(f"Candle batch loaded: {len(candles)} candles.")
                
                if not candles:
                    self.state.status = ReplayStatus.COMPLETED
                    logger.info("Replay completed successfully.")
                    break
                    
                for db_candle in candles:
                    # Check state before yielding next candle
                    await self._handle_speed_and_state()
                    
                    # Convert to NormalizedCandle
                    normalized = NormalizedCandle(
                        symbol=db_candle.symbol,
                        timeframe=db_candle.timeframe,
                        timestamp=db_candle.timestamp,
                        open=db_candle.open,
                        high=db_candle.high,
                        low=db_candle.low,
                        close=db_candle.close,
                        volume=db_candle.volume,
                        source=db_candle.source
                    )
                    
                    # Update progress tracking
                    self.state.current_time = normalized.timestamp
                    self.state.current_symbol = normalized.symbol
                    self.state.candles_processed += 1
                    
                    # Log every 1000 candles for progress visibility
                    if self.state.candles_processed % 1000 == 0:
                        logger.info(f"Replay progress: {self.state.current_time} - {self.state.current_symbol}")
                    
                    yield normalized
                    
                offset += batch_size
                
        finally:
            self._db.close()

    def _fetch_candle_batch(self, limit: int, offset: int) -> list[MarketCandle]:
        """Synchronously fetch a batch of candles, ordered chronologically."""
        return self._db.query(MarketCandle).filter(
            MarketCandle.symbol.in_(self.config.symbols),
            MarketCandle.timeframe == self.config.timeframe,
            MarketCandle.timestamp >= self.config.start_time,
            MarketCandle.timestamp <= self.config.end_time
        ).order_by(
            asc(MarketCandle.timestamp),
            asc(MarketCandle.symbol)
        ).offset(offset).limit(limit).all()

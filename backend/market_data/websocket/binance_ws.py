import asyncio
import json
import logging
import websockets
from sqlalchemy.dialects.postgresql import insert
from typing import Dict, Any

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database import SessionLocal
from market_data.storage.models import MarketCandle
from market_data.normalizers.binance import BinanceNormalizer

import ssl

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BinanceWebSocket")

# In-memory cache to replace Redis for avoiding overengineering
LATEST_PRICES: Dict[str, float] = {}

class BinanceWSClient:
    def __init__(self):
        self.normalizer = BinanceNormalizer()
        
    def store_closed_candle(self, candle_dict: dict):
        """Synchronously store a closed candle into PostgreSQL."""
        db = SessionLocal()
        try:
            stmt = insert(MarketCandle).values([candle_dict])
            on_conflict_stmt = stmt.on_conflict_do_nothing(
                index_elements=['symbol', 'timeframe', 'timestamp', 'source']
            )
            db.execute(on_conflict_stmt)
            db.commit()
            logger.info(f"Stored closed candle for {candle_dict['symbol']} at {candle_dict['timestamp']}")
        except Exception as e:
            logger.error(f"Failed to store closed candle: {e}")
            db.rollback()
        finally:
            db.close()

    async def handle_message(self, message: str):
        """Parse incoming WS message, update cache, and trigger storage if closed."""
        try:
            payload = json.loads(message)
            
            # Ensure it's a kline event
            if payload.get("e") != "kline":
                return
                
            candle, is_closed = self.normalizer.normalize_ws_kline(payload)
            
            # Update fast in-memory cache
            LATEST_PRICES[candle.symbol] = candle.close
            
            # If candle closed, write to permanent storage
            if is_closed:
                # Use asyncio.to_thread to prevent the synchronous database insert from blocking the WebSocket stream
                await asyncio.to_thread(self.store_closed_candle, candle.model_dump())
                
        except Exception as e:
            logger.error(f"Error handling WS message: {e}")

    async def start_stream(self, symbols: list, timeframe: str = "1m"):
        """Connect to Binance and stream live data."""
        # Format streams for Binance e.g. btcusdt@kline_1m
        streams = [f"{sym.lower()}@kline_{timeframe}" for sym in symbols]
        stream_path = "/".join(streams)
        
        ws_url = f"wss://stream.binance.com:9443/ws/{stream_path}"
        logger.info(f"Connecting to Binance WS: {ws_url}")
        
        # Setup SSL context to bypass verification if needed (common in local environments)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        while True:
            try:
                async with websockets.connect(ws_url, ssl=ssl_context) as ws:
                    logger.info("Successfully connected to Binance WebSocket")
                    while True:
                        msg = await ws.recv()
                        await self.handle_message(msg)
            except websockets.exceptions.ConnectionClosed as e:
                logger.warning(f"WebSocket closed: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"WebSocket error: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

# Global instance for FastAPI integration
ws_client = BinanceWSClient()

if __name__ == "__main__":
    symbols_to_track = ["BTCUSDT", "ETHUSDT"]
    
    # Run the asyncio event loop
    try:
        asyncio.run(ws_client.start_stream(symbols_to_track, timeframe="1m"))
    except KeyboardInterrupt:
        logger.info("WebSocket client stopped by user.")

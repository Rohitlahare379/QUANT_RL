from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database import get_db
from market_data.storage.models import MarketCandle
from market_data.normalizers.schemas import NormalizedCandle
from market_data.websocket.binance_ws import LATEST_PRICES
from datetime import timezone

router = APIRouter()

@router.get("/status")
def get_market_data_status():
    """
    Health check and status endpoint for the Market Data Layer.
    """
    return {
        "module": "market_data",
        "status": "online",
        "ingestion_active": False, # Placeholder
        "websocket_active": True
    }

@router.get("/candles", response_model=List[NormalizedCandle])
def get_candles(
    symbol: str = Query(..., description="e.g., BTCUSDT"),
    timeframe: str = Query("1m", description="1m, 5m, 1h"),
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Fetch recent paginated candles for a specific symbol and timeframe."""
    candles = db.query(MarketCandle).filter(
        MarketCandle.symbol == symbol,
        MarketCandle.timeframe == timeframe
    ).order_by(desc(MarketCandle.timestamp)).offset(offset).limit(limit).all()
    
    return candles

@router.get("/historical", response_model=List[NormalizedCandle])
def get_historical_candles(
    symbol: str = Query(...),
    timeframe: str = Query(...),
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    limit: int = Query(1000, le=5000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Fetch historical candles within a strict date range."""
    candles = db.query(MarketCandle).filter(
        MarketCandle.symbol == symbol,
        MarketCandle.timeframe == timeframe,
        MarketCandle.timestamp >= start_time,
        MarketCandle.timestamp <= end_time
    ).order_by(MarketCandle.timestamp).offset(offset).limit(limit).all()
    
    return candles

@router.get("/latest-price")
def get_latest_price(
    symbol: str = Query(..., description="e.g., BTCUSDT"),
    db: Session = Depends(get_db)
):
    """Quick lookup for the most recent close price of an asset, checking live memory cache first."""
    # 1. Check ultra-fast live WebSocket memory cache
    if symbol in LATEST_PRICES:
        return {
            "symbol": symbol,
            "price": LATEST_PRICES[symbol],
            "timestamp": datetime.now(timezone.utc),
            "source": "live_websocket_cache"
        }
        
    # 2. Fallback to database if WebSocket hasn't caught a tick yet
    candle = db.query(MarketCandle).filter(
        MarketCandle.symbol == symbol
    ).order_by(desc(MarketCandle.timestamp)).first()
    
    if not candle:
        raise HTTPException(status_code=404, detail="No price data found for symbol")
        
    return {
        "symbol": candle.symbol,
        "price": candle.close,
        "timestamp": candle.timestamp,
        "source": "database"
    }

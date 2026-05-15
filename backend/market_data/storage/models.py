from sqlalchemy import Column, Integer, String, Float, DateTime, Index, UniqueConstraint
from sqlalchemy.sql import func
from database import Base

class MarketCandle(Base):
    __tablename__ = "market_candles"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False) # e.g. BTCUSDT, ETHUSDT
    timeframe = Column(String, index=True, nullable=False) # e.g. 1m, 1h, 1d
    timestamp = Column(DateTime(timezone=True), index=True, nullable=False)
    
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    
    source = Column(String, nullable=False) # e.g. binance, kaggle
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Compound index for extremely fast timeseries querying
    __table_args__ = (
        Index('ix_market_candles_sym_tf_ts', 'symbol', 'timeframe', 'timestamp'),
        # Ensure we don't insert duplicate candles for the same exact interval and source
        UniqueConstraint('symbol', 'timeframe', 'timestamp', 'source', name='uq_candle_source'),
    )

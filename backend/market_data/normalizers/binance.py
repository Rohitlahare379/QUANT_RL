from typing import List, Any
from datetime import datetime, timezone
from .base import BaseNormalizer
from .schemas import NormalizedCandle

class BinanceNormalizer(BaseNormalizer):
    """
    Normalizes Binance Kline API responses.
    Binance returns arrays: [open_time, open, high, low, close, volume, close_time, quote_asset_volume, trades, taker_buy_base, taker_buy_quote, ignore]
    """
    
    def __init__(self, source_name: str = "binance"):
        self.source = source_name

    def normalize(self, raw_data: List[List[Any]], symbol: str, timeframe: str) -> List[NormalizedCandle]:
        if not raw_data:
            return []
            
        normalized_candles = []
        for kline in raw_data:
            # Kline[0] is the open time in milliseconds
            open_time_ms = kline[0]
            timestamp = datetime.fromtimestamp(open_time_ms / 1000.0, tz=timezone.utc)
            
            candle = NormalizedCandle(
                symbol=symbol,
                timeframe=timeframe,
                timestamp=timestamp,
                open=float(kline[1]),
                high=float(kline[2]),
                low=float(kline[3]),
                close=float(kline[4]),
                volume=float(kline[5]),
                source=self.source
            )
            normalized_candles.append(candle)
            
        return normalized_candles

    def normalize_ws_kline(self, payload: dict) -> tuple[NormalizedCandle, bool]:
        """
        Normalizes a single Binance WebSocket kline payload.
        Returns the NormalizedCandle and a boolean indicating if the candle is closed.
        """
        k = payload.get("k", {})
        
        timestamp = datetime.fromtimestamp(k.get("t") / 1000.0, tz=timezone.utc)
        
        candle = NormalizedCandle(
            symbol=k.get("s"),
            timeframe=k.get("i"),
            timestamp=timestamp,
            open=float(k.get("o")),
            high=float(k.get("h")),
            low=float(k.get("l")),
            close=float(k.get("c")),
            volume=float(k.get("v")),
            source=self.source
        )
        
        is_closed = k.get("x", False)
        return candle, is_closed

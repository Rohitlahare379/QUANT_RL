from pydantic import BaseModel, ConfigDict
from datetime import datetime

class NormalizedCandle(BaseModel):
    symbol: str
    timeframe: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    source: str

    model_config = ConfigDict(from_attributes=True)

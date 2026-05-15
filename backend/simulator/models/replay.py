from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ReplayStatus(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"

class ReplayConfig(BaseModel):
    symbols: List[str]
    timeframe: str = "1h"
    start_time: datetime
    end_time: datetime
    # Replay speed: multiplier for real-time (e.g. 1.0 = real time, 100.0 = 100x speed)
    # A value of 0.0 means process as fast as possible (no artificial sleep)
    speed_multiplier: float = 0.0 

class ReplayState(BaseModel):
    status: ReplayStatus = ReplayStatus.STOPPED
    current_time: Optional[datetime] = None
    current_symbol: Optional[str] = None
    candles_processed: int = 0

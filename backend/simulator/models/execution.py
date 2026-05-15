from datetime import datetime
from typing import Optional
from pydantic import BaseModel

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from simulator.signals.enums import Signal

class ExecutionConfig(BaseModel):
    fees_percent: float = 0.001       # 0.1% default exchange fee
    slippage_percent: float = 0.0005  # 0.05% default slippage
    latency_ms: int = 50              # execution delay simulation (for future tracking)

class ExecutionRecord(BaseModel):
    """
    Structured trade record as specified for realistic simulated trading logs.
    """
    timestamp: datetime
    symbol: str
    signal: Signal
    execution_price: float
    slippage: float
    fees: float
    quantity: float
    resulting_balance: float

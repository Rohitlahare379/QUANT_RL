from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from simulator.signals.enums import Signal

class OpenPosition(BaseModel):
    symbol: str
    entry_price: float
    size: float
    entry_time: datetime
    side: Signal  # Signal.BUY or Signal.SELL indicating long/short

class TradeRecord(BaseModel):
    symbol: str
    entry_price: float
    exit_price: float
    size: float
    entry_time: datetime
    exit_time: datetime
    pnl: float
    pnl_percent: float
    side: Signal

class PortfolioState(BaseModel):
    initial_balance: float
    current_balance: float
    available_cash: float
    open_positions: Dict[str, OpenPosition] = Field(default_factory=dict)
    
    @property
    def total_equity(self) -> float:
        """
        Calculate total equity: available cash + current value of open positions.
        This would require the current market price of assets, so it might need
        a method rather than a simple property in a real implementation.
        """
        return self.current_balance

class SimulationState(BaseModel):
    strategy_name: str
    start_time: datetime
    end_time: datetime
    portfolio: PortfolioState
    trade_history: List[TradeRecord] = Field(default_factory=list)
    is_completed: bool = False

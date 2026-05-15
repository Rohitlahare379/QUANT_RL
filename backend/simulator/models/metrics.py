from pydantic import BaseModel

class SimulationSummary(BaseModel):
    """
    Structured summary of a completed simulation's historical performance.
    """
    total_return: float
    win_rate: float
    trade_count: int
    max_drawdown: float
    sharpe_ratio: float
    average_trade_return: float
    profit_factor: float

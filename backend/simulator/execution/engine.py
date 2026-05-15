import logging

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from simulator.signals.enums import Signal
from simulator.models.execution import ExecutionConfig
from market_data.normalizers.schemas import NormalizedCandle

logger = logging.getLogger("ExecutionEngine")

class ExecutionEngine:
    """
    Simulates the mechanics of order execution.
    Applies slippage and calculates trading fees.
    """
    def __init__(self, config: ExecutionConfig):
        self.config = config

    def execute_order(self, signal: Signal, candle: NormalizedCandle, quantity: float) -> dict:
        """
        Simulates an order fill at the candle's close price, adjusted for slippage and fees.
        Returns a dictionary with execution details.
        """
        base_price = candle.close
        
        # Calculate slippage based on side
        # Buy: price goes up (we pay more). Sell: price goes down (we receive less)
        if signal == Signal.BUY:
            execution_price = base_price * (1 + self.config.slippage_percent)
        elif signal == Signal.SELL:
            execution_price = base_price * (1 - self.config.slippage_percent)
        else:
            execution_price = base_price

        slippage_value = abs(execution_price - base_price) * quantity
        
        # Calculate fees on the notional value
        notional_value = execution_price * quantity
        fees = notional_value * self.config.fees_percent
        
        return {
            "execution_price": execution_price,
            "slippage": slippage_value,
            "fees": fees,
            "quantity": quantity
        }

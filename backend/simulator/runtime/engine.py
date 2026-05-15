import logging
from typing import Dict, Any

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from market_data.normalizers.schemas import NormalizedCandle
from simulator.interfaces.strategy import Strategy
from simulator.signals.enums import Signal
from simulator.models.runtime import StrategyDecision

logger = logging.getLogger("StrategyRuntime")

import pandas as pd

class StrategyRunner:
    """
    Executes a specific strategy instance against incoming market candles.
    Maintains isolated state and safely handles execution exceptions.
    """
    def __init__(self, strategy: Strategy, strategy_name: str = "Unknown"):
        self.strategy = strategy
        self.strategy_name = strategy_name
        self._history_list = []
        
    def process_candle(self, candle: NormalizedCandle) -> StrategyDecision:
        """
        Passes a candle to the strategy, safely catches any issues, 
        and packages the result into a structured StrategyDecision.
        """
        # Maintain rolling history for indicators
        self._history_list.append({
            'open': candle.open,
            'high': candle.high,
            'low': candle.low,
            'close': candle.close,
            'volume': candle.volume,
            'timestamp': candle.timestamp
        })
        
        # We cap the history to save memory, e.g., 200 periods is enough for most MAs
        if len(self._history_list) > 500:
            self._history_list.pop(0)
            
        hist_df = pd.DataFrame(self._history_list)
        
        # Default to holding if something crashes
        final_signal = Signal.HOLD
        reasoning = "Executed successfully"
        
        try:
            # 1. Execute strategy
            logger.debug(f"[{self.strategy_name}] Processing {candle.symbol} at {candle.timestamp}")
            
            import inspect
            sig = inspect.signature(self.strategy.on_candle)
            kwargs = {}
            if 'hist' in sig.parameters:
                kwargs['hist'] = hist_df
            elif 'history' in sig.parameters:
                kwargs['history'] = hist_df
                
            # Many user strategies assume candle is a dictionary
            candle_data = candle.model_dump()
            
            result = self.strategy.on_candle(candle_data, **kwargs)
            
            # 2. Validate signal type
            if isinstance(result, Signal):
                final_signal = result
            else:
                logger.warning(f"[{self.strategy_name}] Invalid signal returned: {result}. Defaulting to HOLD.")
                reasoning = f"Invalid return type: {type(result).__name__}"
                
        except Exception as e:
            logger.error(f"[{self.strategy_name}] Crash during execution: {e}", exc_info=True)
            reasoning = f"Strategy crashed: {str(e)}"
            
        # 3. Emit structured decision
        decision = StrategyDecision(
            signal=final_signal,
            timestamp=candle.timestamp,
            symbol=candle.symbol,
            reasoning=reasoning,
            strategy_name=self.strategy_name
        )
        
        if final_signal != Signal.HOLD:
            logger.info(f"[{self.strategy_name}] Generated {final_signal.name} for {candle.symbol} at {candle.timestamp}")
            
        return decision

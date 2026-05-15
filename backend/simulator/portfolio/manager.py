import logging
from typing import List, Optional

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from market_data.normalizers.schemas import NormalizedCandle
from simulator.models.runtime import StrategyDecision
from simulator.signals.enums import Signal
from simulator.models.state import PortfolioState, OpenPosition, TradeRecord
from simulator.models.execution import ExecutionRecord, ExecutionConfig
from simulator.execution.engine import ExecutionEngine

logger = logging.getLogger("PortfolioManager")

class PortfolioManager:
    """
    Simulates paper trading realistically by managing account balance,
    single active positions, and compiling structured trade logs.
    """
    def __init__(self, initial_balance: float = 10000.0, execution_config: Optional[ExecutionConfig] = None):
        self.state = PortfolioState(
            initial_balance=initial_balance,
            current_balance=initial_balance,
            available_cash=initial_balance
        )
        self.execution_engine = ExecutionEngine(execution_config or ExecutionConfig())
        self.trade_logs: List[ExecutionRecord] = []
        self.realized_pnls: List[float] = []
        # Support single active position initially
        self.default_position_size_usd = 1000.0 

    def process_decision(self, decision: StrategyDecision, current_candle: NormalizedCandle) -> Optional[ExecutionRecord]:
        """
        Receives a strategy decision, evaluates if an action should be taken based
        on current portfolio state, and logs the resulting execution.
        """
        if decision.signal == Signal.HOLD:
            self._update_unrealized_pnl(current_candle)
            return None

        # Check if we already have a position
        has_position = decision.symbol in self.state.open_positions
        current_position = self.state.open_positions.get(decision.symbol)

        # Logic for a single active position model:
        # If we have a position and get the same signal (e.g. BUY while long), do nothing.
        # If we have a position and get an opposite signal, close the position.
        # If we don't have a position, open one.
        
        execution_record = None
        
        if has_position:
            if current_position.side == decision.signal:
                # Already in this direction
                self._update_unrealized_pnl(current_candle)
                return None
            else:
                # Close existing position
                execution_record = self._close_position(decision, current_candle, current_position)
        else:
            # Open new position
            execution_record = self._open_position(decision, current_candle)
            
        self._update_unrealized_pnl(current_candle)
        return execution_record

    def _open_position(self, decision: StrategyDecision, candle: NormalizedCandle) -> Optional[ExecutionRecord]:
        # Determine quantity (simplistic fixed USD size for now)
        if self.state.available_cash < self.default_position_size_usd:
            logger.warning("Insufficient funds to open position.")
            return None
            
        quantity = self.default_position_size_usd / candle.close
        
        # Execute order via Execution Engine
        exec_details = self.execution_engine.execute_order(decision.signal, candle, quantity)
        
        # Update portfolio
        cost_basis = exec_details["execution_price"] * quantity
        total_cost = cost_basis + exec_details["fees"]
        self.state.available_cash -= total_cost
        
        new_position = OpenPosition(
            symbol=decision.symbol,
            entry_price=exec_details["execution_price"],
            size=quantity,
            entry_time=decision.timestamp,
            side=decision.signal
        )
        self.state.open_positions[decision.symbol] = new_position
        
        # Create record
        record = ExecutionRecord(
            timestamp=decision.timestamp,
            symbol=decision.symbol,
            signal=decision.signal,
            execution_price=exec_details["execution_price"],
            slippage=exec_details["slippage"],
            fees=exec_details["fees"],
            quantity=quantity,
            resulting_balance=self.state.current_balance # Balance only changes on realized PnL
        )
        self.trade_logs.append(record)
        logger.info(f"OPENED {decision.signal.name} position for {decision.symbol} at {exec_details['execution_price']}")
        return record

    def _close_position(self, decision: StrategyDecision, candle: NormalizedCandle, position: OpenPosition) -> ExecutionRecord:
        # Execute order via Execution Engine (opposite of entry)
        # Note: if we were Long (BUY), we now SELL to close. decision.signal is the new desired state, 
        # but to close a BUY we issue a SELL execution. decision.signal here is technically the opposite of position.side.
        exec_details = self.execution_engine.execute_order(decision.signal, candle, position.size)
        
        # Calculate PnL
        if position.side == Signal.BUY:
            # Long position profit: Exit value - Entry cost
            pnl = (exec_details["execution_price"] - position.entry_price) * position.size
        else:
            # Short position profit: Entry cost - Exit value
            pnl = (position.entry_price - exec_details["execution_price"]) * position.size
            
        realized_pnl = pnl - exec_details["fees"]
        
        # Update portfolio
        cost_basis = position.entry_price * position.size
        self.state.available_cash += (cost_basis + realized_pnl)
        self.state.current_balance += realized_pnl
        
        # Record realized PnL
        self.realized_pnls.append(realized_pnl)
        logger.info(f"[Portfolio] REALIZED PNL RECORDED: {realized_pnl:.4f}")
        
        del self.state.open_positions[decision.symbol]
        
        # Create record
        record = ExecutionRecord(
            timestamp=decision.timestamp,
            symbol=decision.symbol,
            signal=decision.signal,
            execution_price=exec_details["execution_price"],
            slippage=exec_details["slippage"],
            fees=exec_details["fees"],
            quantity=position.size,
            resulting_balance=self.state.current_balance
        )
        self.trade_logs.append(record)
        logger.info(f"CLOSED position for {decision.symbol} at {exec_details['execution_price']}. Realized PnL: {realized_pnl:.2f}")
        return record

    def _update_unrealized_pnl(self, current_candle: NormalizedCandle):
        """Updates the portfolio equity curve by calculating unrealized PnL for all open positions."""
        total_unrealized_pnl = 0.0
        
        # We need current prices for all open positions to calculate equity.
        # In a single-asset replay, we only have the current_candle for the traded asset.
        # If there are positions in other assets, they would be static or we'd need their last price.
        # For now, we update the pnl for the current_candle's symbol and assume others are at their last known price.
        
        for symbol, position in self.state.open_positions.items():
            if symbol == current_candle.symbol:
                # Update with newest price
                if position.side == Signal.BUY:
                    pnl = (current_candle.close - position.entry_price) * position.size
                else:
                    pnl = (position.entry_price - current_candle.close) * position.size
                total_unrealized_pnl += pnl
            else:
                # Use a cached price or entry price if not the current symbol
                # In this simulator's current state, we mostly deal with one symbol at a time.
                pass
                 
        # Total equity = available cash + cost basis of all positions + total unrealized pnl
        total_cost_basis = sum(pos.entry_price * pos.size for pos in self.state.open_positions.values())
        self.state.current_balance = self.state.available_cash + total_cost_basis + total_unrealized_pnl

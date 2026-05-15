import logging
import math
from typing import List

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from simulator.models.metrics import SimulationSummary

logger = logging.getLogger("MetricsCalculator")

class MetricsCalculator:
    """
    Evaluates historical strategy performance and calculates standard mathematical 
    financial metrics (Total Return, Win Rate, Sharpe, Max Drawdown, etc.).
    """
    
    @staticmethod
    def calculate(initial_balance: float, final_balance: float, equity_curve: List[float], trade_pnls: List[float]) -> SimulationSummary:
        """
        Calculates all metrics and returns a structured SimulationSummary.
        
        :param initial_balance: The starting portfolio balance.
        :param final_balance: The ending portfolio balance.
        :param equity_curve: A chronologically ordered list of portfolio balances over time.
        :param trade_pnls: A list containing the realized PnL of every completed trade.
        """
        
        trade_count = len(trade_pnls)
        
        # 1. Total Return
        total_return = 0.0
        if initial_balance > 0:
            total_return = ((final_balance - initial_balance) / initial_balance) * 100.0

        # Edge Case: No Trades
        if trade_count == 0:
            logger.info("No trades executed. Returning zeroed metrics.")
            return SimulationSummary(
                total_return=total_return,
                win_rate=0.0,
                trade_count=0,
                max_drawdown=0.0,
                sharpe_ratio=0.0,
                average_trade_return=0.0,
                profit_factor=0.0
            )

        # 2. Win Rate
        winning_trades = sum(1 for pnl in trade_pnls if pnl > 0)
        win_rate = (winning_trades / trade_count) * 100.0

        # 3. Average Trade Return
        average_trade_return = sum(trade_pnls) / trade_count

        # 4. Profit Factor (Gross Profit / Gross Loss)
        gross_profit = sum(pnl for pnl in trade_pnls if pnl > 0)
        gross_loss = abs(sum(pnl for pnl in trade_pnls if pnl < 0))
        profit_factor = float('inf') if gross_loss == 0 else (gross_profit / gross_loss)

        # 5. Max Drawdown
        max_drawdown = 0.0
        peak = initial_balance
        for equity in equity_curve:
            if equity > peak:
                peak = equity
            drawdown = (peak - equity) / peak * 100.0
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        # 6. Sharpe Ratio (Simplified based on trade returns)
        # Assuming risk free rate = 0
        mean_pnl = average_trade_return
        variance = sum((pnl - mean_pnl) ** 2 for pnl in trade_pnls) / trade_count
        std_dev = math.sqrt(variance)
        
        # Prevent division by zero if all trades have the exact same PnL
        sharpe_ratio = 0.0
        if std_dev > 0:
            # Note: This is a simplistic Sharpe over trades, not annualized time periods
            sharpe_ratio = mean_pnl / std_dev 

        summary = SimulationSummary(
            total_return=total_return,
            win_rate=win_rate,
            trade_count=trade_count,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            average_trade_return=average_trade_return,
            profit_factor=profit_factor
        )
        
        logger.info(f"Metrics Calculated: Return: {total_return:.2f}%, Win Rate: {win_rate:.2f}%, Trades: {trade_count}, DD: {max_drawdown:.2f}%")
        return summary

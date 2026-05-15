import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from simulator.loaders.strategy_loader import StrategyLoader

code = """
from simulator.interfaces.strategy import Strategy
from simulator.signals.enums import Signal

class SMACrossoverStrategy(Strategy):
    def __init__(self):
        pass
    def on_candle(self, candle, history):
        pass
"""

res = StrategyLoader.load_from_string(code)
print("Result:", res)

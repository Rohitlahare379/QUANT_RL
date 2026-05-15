---
phase: 9
plan: 1
wave: 1
---

# Plan 9.1: Simulation Metrics and Evaluation Engine

## Objective
Build the Aegis Simulation Metrics Engine to evaluate historical strategy performance using standardized mathematical formulas.

## Context
- .gsd/ROADMAP.md
- backend/simulator/models/execution.py
- backend/simulator/models/state.py

## Tasks

<task type="auto" effort="low">
  <name>Create Metrics Models</name>
  <action>
    Create `backend/simulator/models/metrics.py`.
    Define `SimulationSummary` Pydantic model with fields:
    - total_return: float
    - win_rate: float
    - trade_count: int
    - max_drawdown: float
    - sharpe_ratio: float
    - average_trade_return: float
    - profit_factor: float
  </action>
  <verify>python -c "import sys; sys.path.append('backend'); from simulator.models.metrics import SimulationSummary"</verify>
  <done>Model successfully defines the structured summary format.</done>
</task>

<task type="auto" effort="high">
  <name>Implement Metrics Calculator</name>
  <action>
    Create `backend/simulator/metrics/calculator.py`.
    Build `MetricsCalculator` class or standalone functions that:
    - Receive a list of completed trades and portfolio history/equity curve.
    - Calculate total return, win rate, trade count, max drawdown, Sharpe ratio, average trade return, and profit factor.
    - Handle edge cases (e.g. 0 trades, dividing by zero).
    - Return a populated `SimulationSummary` object.
    - Include summary logging to output the calculated metrics cleanly.
  </action>
  <verify>python -c "import sys; sys.path.append('backend'); from simulator.metrics.calculator import MetricsCalculator"</verify>
  <done>Metrics Calculator successfully processes execution records into a SimulationSummary.</done>
</task>

## Success Criteria
- [ ] Returns structured SimulationSummary correctly calculated from generic execution records.
- [ ] Completely decoupled from replay and strategy runtime logic.
- [ ] Edge cases (no trades, straight losses) are handled safely without exceptions.

---
phase: 8
plan: 1
wave: 1
---

# Plan 8.1: Portfolio and Trade Simulation Engine

## Objective
Build the Aegis Portfolio and Trade Simulation Engine to convert strategy signals into realistic simulated trading activity.

## Context
- .gsd/ROADMAP.md
- backend/simulator/models/state.py
- backend/simulator/models/runtime.py

## Tasks

<task type="auto" effort="low">
  <name>Create Execution Models</name>
  <action>
    Create `backend/simulator/models/execution.py`.
    Define `ExecutionConfig` (fees_percent, slippage_percent, default_position_size).
    Define `ExecutionRecord` containing the requested structured trade records:
    (timestamp, symbol, signal, execution_price, slippage, fees, quantity, resulting_balance).
  </action>
  <verify>python -c "import sys; sys.path.append('backend'); from simulator.models.execution import ExecutionRecord"</verify>
  <done>Models are successfully defined and importable.</done>
</task>

<task type="auto" effort="high">
  <name>Implement Execution and Portfolio Logic</name>
  <action>
    Create `backend/simulator/execution/engine.py`.
    Build `ExecutionEngine` that:
    - Accepts `ExecutionConfig`.
    - Simulates order execution (applying slippage and calculating fees).
    - Returns simulated execution details.
    
    Create `backend/simulator/portfolio/manager.py`.
    Build `PortfolioManager` that:
    - Maintains `PortfolioState`.
    - Handles single active position logic (closing existing position if signal flips).
    - Calculates realized and unrealized PnL.
    - Records `ExecutionRecord` logs.
  </action>
  <verify>python -c "import sys; sys.path.append('backend'); from simulator.portfolio.manager import PortfolioManager"</verify>
  <done>Portfolio Manager realistically simulates balances and positions based on strategy signals.</done>
</task>

## Success Criteria
- [ ] Realistic execution factors (slippage/fees) are applied to signals.
- [ ] Portfolio accurately tracks balances and single active positions.
- [ ] Output trades match the required ExecutionRecord structure.
- [ ] No monolithic coupling; logic is split properly.

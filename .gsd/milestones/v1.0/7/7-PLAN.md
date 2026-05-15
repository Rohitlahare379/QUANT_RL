---
phase: 7
plan: 1
wave: 1
---

# Plan 7.1: Strategy Runtime Execution Engine

## Objective
Build the Aegis Strategy Runtime Execution Engine to transform replayed candles into structured trading signals while ensuring execution safety and modularity.

## Context
- .gsd/ROADMAP.md
- backend/simulator/interfaces/strategy.py
- backend/simulator/signals/enums.py
- backend/simulator/models/runtime.py (To be created)

## Tasks

<task type="auto" effort="low">
  <name>Create Runtime Models</name>
  <action>
    Create `backend/simulator/models/runtime.py`.
    Define `StrategyDecision` Pydantic model with fields:
    - signal: Signal enum
    - timestamp: datetime
    - symbol: str
    - reasoning: str (optional)
    - strategy_name: str
  </action>
  <verify>python -c "import sys; sys.path.append('backend'); from simulator.models.runtime import StrategyDecision"</verify>
  <done>Model successfully defines the structured signal format.</done>
</task>

<task type="auto" effort="medium">
  <name>Implement Strategy Runner</name>
  <action>
    Create `backend/simulator/runtime/engine.py`.
    Build `StrategyRunner` class that:
    - Accepts an instantiated `Strategy`.
    - Implements `process_candle(candle: NormalizedCandle) -> StrategyDecision`.
    - Isolates state by not sharing data across different runner instances.
    - Uses a try-except block to safely handle strategy execution errors, returning HOLD or raising a clear exception.
    - Includes proper runtime logging (strategy execution logs, signal generation, invalid signals).
  </action>
  <verify>python -c "import sys; sys.path.append('backend'); from simulator.runtime.engine import StrategyRunner"</verify>
  <done>StrategyRunner securely executes strategy and returns structured StrategyDecision.</done>
</task>

## Success Criteria
- [ ] Runner strictly uses NormalizedCandle and returns StrategyDecision.
- [ ] Invalid signal outputs or internal strategy crashes are caught safely.
- [ ] No monolithic coupling with portfolio or replay logic.

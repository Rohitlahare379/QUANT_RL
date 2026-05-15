---
phase: 10
plan: 1
wave: 1
---

# Plan 10.1: Room 1 and Simulator Integration

## Objective
Connect Room 1 frontend to Room 2 simulation backend via websockets, streaming live historical replay execution and visualizing simulation metrics.

## Context
- .gsd/ROADMAP.md
- backend/main.py
- frontend/src/App.tsx

## Tasks

<task type="auto" effort="high">
  <name>Build Simulator WebSocket API</name>
  <action>
    Create `backend/simulator/api/router.py`.
    Implement a FastAPI WebSocket endpoint `/ws/simulate`.
    The endpoint should:
    - Receive strategy code and simulation parameters from the frontend.
    - Instantiate the `StrategyLoader`, `ReplayEngine`, `StrategyRunner`, and `PortfolioManager`.
    - Loop over the `stream_candles()` async generator from `ReplayEngine`.
    - Execute the strategy via `StrategyRunner`.
    - Pass decisions to `PortfolioManager`.
    - Stream JSON updates (candle info, trades, signals, balance) back to the WebSocket client.
    - Calculate and send final metrics via `MetricsCalculator` when complete.
    Hook this router into `backend/main.py`.
  </action>
  <verify>grep "/ws/simulate" backend/main.py || grep "simulator_router" backend/main.py</verify>
  <done>Simulator WebSocket endpoint is operational and integrates all engines.</done>
</task>

<task type="auto" effort="high">
  <name>Connect Frontend Simulator UI</name>
  <action>
    Update `frontend/src/App.tsx`.
    - Wire the "Run strategy" button to open a WebSocket connection to `/ws/simulate`.
    - Send strategy code from the Monaco editor and parameters via WebSocket.
    - Create React state hooks for `simulationProgress`, `trades`, `signals`, `balance`, and `metrics`.
    - Build UI panels below or beside the editor to visualize trade history, balance, and final metrics.
    - Add Play/Pause/Stop control buttons that send control commands via WebSocket to the backend.
  </action>
  <verify>grep "WebSocket" frontend/src/App.tsx</verify>
  <done>Frontend seamlessly streams real-time simulation updates and displays interactive controls.</done>
</task>

## Success Criteria
- [ ] User can execute strategy and see live updates.
- [ ] Backend wires all decoupled engines correctly via WebSocket streaming.
- [ ] UI stays professional and integrates with existing styling.

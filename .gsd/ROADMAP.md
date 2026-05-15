# ROADMAP.md

> **Current Phase**: Phase 2 Planning
> **Milestone**: v1.0

## Must-Haves (from SPEC)
- [ ] React + Vite frontend with Tailwind and shadcn UI.
- [ ] Monaco editor with Python syntax support.
- [ ] Sidebar for strategy list and loadable templates (RSI, Momentum, Mean Reversion).
- [ ] UI buttons for Create, Save, and Validate strategy.
- [ ] FastAPI backend endpoint with PostgreSQL integration.

## Phases

### Phase 1: Foundation Setup
**Status**: ✅ Complete
**Objective**: Scaffold the React + Vite frontend (Tailwind + shadcn UI) and the FastAPI + PostgreSQL backend.

### Phase 2: Core Workshop UI
**Status**: ✅ Complete
**Objective**: Build the application layout (sidebar, main panel, minimal professional interface) and functional buttons (Create, Save, Validate).

### Phase 3: Monaco Editor & Templates
**Status**: ✅ Complete
**Objective**: Integrate Monaco editor with Python syntax support and implement the logic to load strategy templates (RSI, Momentum, Mean Reversion).

### Phase 4: Backend Integration
**Status**: ✅ Complete
**Objective**: Connect the frontend to the FastAPI backend to fetch/save strategies and store them in PostgreSQL.

### Phase 5: Data Layer Foundation
**Status**: ✅ Complete
**Objective**: Build the backend foundation for the Aegis market data layer with modular architecture, PostgreSQL, and env variables.

### Phase 6: Historical Replay Engine (Room 2)
**Status**: ✅ Complete
**Objective**: Build the Aegis Historical Replay Engine to sequentially replay normalized market candles for strategy backtesting.
**Depends on**: Phase 5

### Phase 7: Strategy Runtime Execution Engine
**Status**: ✅ Complete
**Objective**: Execute user-created strategies against replayed historical candles and emit structured signals.
**Depends on**: Phase 6

### Phase 8: Portfolio and Trade Simulation Engine
**Status**: ✅ Complete
**Objective**: Simulate realistic paper trading, managing account balance, positions, and execution factors.
**Depends on**: Phase 7

### Phase 9: Simulation Metrics and Evaluation Engine
**Status**: ✅ Complete
**Objective**: Evaluate historical strategy performance by calculating metrics like Sharpe ratio, max drawdown, and win rate.
**Depends on**: Phase 8

### Phase 10: Room 1 and Simulator Integration
**Status**: ✅ Complete
**Objective**: Connect Room 1 frontend to the backend simulator via websockets to stream historical strategy execution.
**Depends on**: Phase 9

**Tasks**:
- [x] Build backend friction pipeline
- [x] Integrate Room 1 & 2 UIs
- [x] Enable WS Streaming & React State mapping

**Verification**:
- ✅ Simulator updates correctly without crashing
- ✅ Strategy editor successfully validates via AST parsing

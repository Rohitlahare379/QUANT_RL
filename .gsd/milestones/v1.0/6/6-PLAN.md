---
phase: 6
plan: 1
wave: 1
---

# Plan 6.1: Replay Engine Foundation

## Objective
Build the Historical Replay Engine to sequentially yield market candles without loading the entire dataset into memory.

## Context
- .gsd/ROADMAP.md
- backend/simulator/models/state.py
- backend/market_data/storage/models.py

## Tasks

<task type="auto" effort="medium">
  <name>Create Replay State Models</name>
  <action>
    Create `backend/simulator/models/replay.py`.
    Define `ReplayStatus` enum (PLAYING, PAUSED, STOPPED).
    Define `ReplayConfig` (symbols, timeframe, start_time, end_time, speed).
    Define `ReplayState` (current_time, current_candle_info, status).
  </action>
  <verify>python -c "import sys; sys.path.append('backend'); from simulator.models.replay import ReplayStatus"</verify>
  <done>Models are successfully defined and importable.</done>
</task>

<task type="auto" effort="high">
  <name>Implement Replay Engine Generator</name>
  <action>
    Create `backend/simulator/replay/engine.py`.
    Build `ReplayEngine` class that:
    - Accepts `ReplayConfig`.
    - Manages `ReplayState`.
    - Uses an async generator `stream_candles()` to fetch `MarketCandle` from the DB incrementally (using yield).
    - Supports pause/stop session controls (using `asyncio.sleep` to simulate replay speed and await unpausing).
    - Translates raw `MarketCandle` to `NormalizedCandle`.
  </action>
  <verify>python -c "import sys; sys.path.append('backend'); from simulator.replay.engine import ReplayEngine"</verify>
  <done>ReplayEngine yields sequential candles dynamically without breaking memory limits.</done>
</task>

## Success Criteria
- [ ] Engine yields candles chronologically.
- [ ] Memory footprint remains small via pagination/yielding.
- [ ] Replay can be paused and resumed.

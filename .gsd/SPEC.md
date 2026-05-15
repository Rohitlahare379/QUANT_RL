# SPEC.md — Project Specification

> **Status**: `FINALIZED`

## Vision
Room 1 of Aegis: A professional, minimal strategy workshop interface. It features a React + Vite frontend with a Python-enabled Monaco editor for quantitative strategy development, backed by a FastAPI endpoint and PostgreSQL for persistence.

## Goals
1. Setup a React + Vite frontend with Tailwind CSS and shadcn UI in a clean, modular folder structure.
2. Implement a strategy workshop interface containing a sidebar (strategy list) and a main Monaco editor panel (with Python syntax support).
3. Provide loadable strategy templates (RSI, Momentum, Mean Reversion).
4. Implement UI controls: Create strategy, Save strategy, Validate strategy.
5. Build a FastAPI backend endpoint integrated with PostgreSQL to handle saving strategies.

## Non-Goals (Out of Scope)
- Authentication
- AI generation
- Real execution
- Websocket feeds
- Advanced IDE features

## Users
Quantitative developers and strategists building and validating algorithmic trading strategies before deployment.

## Constraints
- Minimal and professional interface design.
- Python syntax support specifically for the Monaco editor.
- Must strictly use the Get Shit Done (GSD) workflow framework for all development steps.

## Success Criteria
- [ ] Frontend successfully renders with sidebar, Monaco editor, and control buttons.
- [ ] Monaco editor properly highlights Python syntax.
- [ ] Strategy templates load correctly into the editor when selected.
- [ ] FastAPI backend successfully receives and saves strategy data to the PostgreSQL database.

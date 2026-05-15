---
phase: 5
plan: 1
wave: 1
---

# Plan 5.1: Data Layer Foundation

## Objective
Build the backend foundation for the Aegis market data layer using a modular architecture with PostgreSQL and environment variables.

## Context
- .gsd/ROADMAP.md
- backend/main.py

## Tasks

<task type="auto" effort="low">
  <name>Create Folder Structure</name>
  <action>
    Create the market_data module with subfolders for ingestion, websocket, normalizers, storage, replay, and api.
  </action>
  <verify>ls -l backend/market_data</verify>
  <done>All 6 required subdirectories exist.</done>
</task>

<task type="auto" effort="medium">
  <name>Setup Configuration & Env Vars</name>
  <action>
    Install `python-dotenv`.
    Create `backend/.env` and `backend/config.py` to securely manage the DATABASE_URL.
    Update `backend/database.py` to use settings from `config.py`.
  </action>
  <verify>grep dotenv backend/config.py</verify>
  <done>Database connection uses environment variables instead of hardcoded strings.</done>
</task>

<task type="auto" effort="medium">
  <name>API Routing Setup</name>
  <action>
    Create `backend/market_data/api/router.py` with a basic health/status endpoint for the data layer.
    Include this router in the main FastAPI application in `backend/main.py`.
  </action>
  <verify>grep "market_data" backend/main.py</verify>
  <done>The market_data router is hooked into the main FastAPI app.</done>
</task>

## Success Criteria
- [ ] Folder structure is modular and strictly follows requirements.
- [ ] `database.py` relies on `config.py` instead of hardcoded strings.
- [ ] Overengineering (Redis, Kafka, microservices) is completely avoided.

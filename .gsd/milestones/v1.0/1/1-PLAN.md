---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Frontend and Backend Scaffolding

## Objective
Scaffold the React + Vite frontend (Tailwind + shadcn UI) and the FastAPI + PostgreSQL backend to establish the foundation of Aegis Room 1.

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md

## Tasks

<task type="auto" effort="medium">
  <name>Initialize React + Vite frontend</name>
  <action>
    Initialize a React application using Vite with TypeScript inside a `frontend` folder.
    Install Tailwind CSS, postcss, and autoprefixer.
    Initialize shadcn UI in the frontend folder.
    Avoid: interactive commands (use non-interactive mode).
  </action>
  <verify>cd frontend && test -f package.json && test -f tailwind.config.js</verify>
  <done>Frontend scaffolding is complete and tailwind/shadcn is ready.</done>
</task>

<task type="auto" effort="medium">
  <name>Initialize FastAPI + PostgreSQL backend</name>
  <action>
    Create a `backend` folder.
    Create a `requirements.txt` containing fastapi, uvicorn, pydantic, sqlalchemy, and psycopg2-binary.
    Create a basic `main.py` entrypoint for FastAPI and a `database.py` for PostgreSQL connection using SQLAlchemy.
  </action>
  <verify>cd backend && test -f main.py && test -f requirements.txt</verify>
  <done>Backend scaffolding is complete with DB connection setup.</done>
</task>

## Success Criteria
- [ ] `frontend` folder exists with Vite + Tailwind configuration.
- [ ] `backend` folder exists with FastAPI entrypoint and SQLAlchemy setup.

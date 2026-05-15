# Aegis: Autonomous Quant Evaluation Platform

Aegis is an AI-native platform for high-fidelity quantitative strategy evaluation, autonomous robustness testing, and intelligent paper trading.

## 🚀 Quick Start (Hackathon Demo Flow)

### 1. Prerequisites
- Python 3.9+
- Node.js 18+
- SQLite (included)

### 2. Environment Setup

#### Backend
Create `backend/.env`:
```env
DATABASE_URL=sqlite:///./aegis.db
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/... (optional)
GENERIC_WEBHOOK_URL=http://localhost:5000/callback (optional)
```

#### Frontend
Create `frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000
```

### 3. Installation

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 4. Running the Platform

**Start Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```
*Verify: `http://localhost:8000/health` should return `{"status": "ok"}`.*

**Start Frontend:**
```bash
cd frontend
npm run dev
```
*Access: `http://localhost:5173`*

---

## 🛠 Project Structure

- **Room 1 (Workshop):** Strategy development using Python SDK. Features a real-time validation pipeline.
- **Room 2 (Simulator):** Triple-portfolio simulation (Ideal, Slippage, Latency) with live WebSocket streaming.
- **Room 3 (Orchestrator):** Multi-agent autonomous evaluation. Sequences Regime Classification, Robustness Testing, and Deployment Decision agents.

## 📊 Demo Workflow
1. **Develop:** Load a template in Room 1 (e.g., RSI).
2. **Validate:** Click **RUN** to perform a syntax and dry-run check.
3. **Simulate:** Navigate to Room 2 and click **RUN SIMULATION**. Observe the live equity curve and friction analysis.
4. **Evaluate:** Once simulated, navigate to Room 3. Click **START AUTONOMOUS WORKFLOW**.
5. **Trace:** Observe the **Causality Trace** as agents analyze the strategy.
6. **Report:** Export the final **Operational Intelligence Report** (PDF/JSON).

---

## 🛡 System Health Checks
Aegis performs the following checks on startup:
- **Environment:** Validates `.env` variables and API keys.
- **Database:** Verifies connectivity to SQLite/PostgreSQL.
- **Market Data:** Checks availability of historical datasets for replay.
- **Orchestrator:** Ensures all AI agents are initialized and reachable.

---
*Built for the 2026 Autonomous Quant Hackathon.*

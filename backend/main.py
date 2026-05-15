from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import asyncio

from database import engine, Base, get_db
import models
import schemas
from market_data.api.router import router as market_data_router
import market_data.storage.models  # Register market_candles table
from market_data.websocket.binance_ws import ws_client
from simulator.api.router import router as simulator_router

# Create database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Launch the Binance WebSocket stream in the background
    symbols = ["BTCUSDT", "ETHUSDT"]
    task = asyncio.create_task(ws_client.start_stream(symbols, timeframe="1m"))
    yield
    # Shutdown: Cancel the WebSocket task gracefully
    task.cancel()

app = FastAPI(title="Aegis Room 1 API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow frontend to access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_data_router, prefix="/api/market-data", tags=["Market Data"])
app.include_router(simulator_router, prefix="/ws", tags=["Simulator"])

@app.get("/")
def read_root():
    return {"message": "Aegis Room 1 Backend is running"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "ok", "database": "connected"}

@app.post("/api/strategies", response_model=schemas.StrategyResponse)
def save_strategy(strategy: schemas.StrategyCreate, db: Session = Depends(get_db)):
    db_strategy = models.Strategy(name=strategy.name, code=strategy.code)
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

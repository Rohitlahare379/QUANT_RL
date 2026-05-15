from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import asyncio

from database import engine, Base, get_db, SessionLocal
from sqlalchemy import text
import models
import schemas
from market_data.api.router import router as market_data_router
import market_data.storage.models  # Register market_candles table
from market_data.websocket.binance_ws import ws_client
from simulator.api.router import router as simulator_router
from orchestrator.runtime import Orchestrator
from orchestrator.context import SharedContext

from config import settings, validate_environment
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("AegisMain")

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Environment Validation
    logger.info("--- Aegis System Startup ---")
    issues = validate_environment()
    if issues:
        for issue in issues:
            logger.error(f"Startup Blocked: {issue}")
        # In a real demo, we might exit, but for local dev we continue with warnings
    
    # 2. Database Connectivity Check
    try:
        # Simple query to verify DB
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connectivity verified.")
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")

    # 3. Market Data Stream Initialization
    symbols = ["BTCUSDT", "ETHUSDT"]
    logger.info(f"Initializing real-time market data streams for: {symbols}")
    task = asyncio.create_task(ws_client.start_stream(symbols, timeframe="1m"))
    
    logger.info("Aegis Orchestrator initialized and ready.")
    yield
    
    # Shutdown
    logger.info("Shutting down market data streams...")
    task.cancel()
    logger.info("Aegis System Shutdown complete.")

app = FastAPI(title="Aegis Autonomous Evaluation Platform", lifespan=lifespan)

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

@app.get("/api/strategies", response_model=list[schemas.StrategyResponse])
def list_strategies(db: Session = Depends(get_db)):
    return db.query(models.Strategy).order_by(models.Strategy.updated_at.desc()).all()

@app.get("/api/strategies/{strategy_id}", response_model=schemas.StrategyResponse)
def get_strategy(strategy_id: int, db: Session = Depends(get_db)):
    db_strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not db_strategy:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Strategy not found")
    return db_strategy

@app.post("/api/strategies", response_model=schemas.StrategyResponse)
def save_strategy(strategy: schemas.StrategyCreate, db: Session = Depends(get_db)):
    # If a strategy with the same name exists, we update it (standard behavior)
    db_strategy = db.query(models.Strategy).filter(models.Strategy.name == strategy.name).first()
    if db_strategy:
        for key, value in strategy.model_dump().items():
            setattr(db_strategy, key, value)
        db.commit()
        db.refresh(db_strategy)
        return db_strategy
        
    new_strategy = models.Strategy(**strategy.model_dump())
    db.add(new_strategy)
    db.commit()
    db.refresh(new_strategy)
    return new_strategy

@app.put("/api/strategies/{strategy_id}", response_model=schemas.StrategyResponse)
def update_strategy(strategy_id: int, strategy: schemas.StrategyCreate, db: Session = Depends(get_db)):
    db_strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not db_strategy:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    for key, value in strategy.model_dump().items():
        setattr(db_strategy, key, value)
        
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@app.patch("/api/strategies/{strategy_id}", response_model=schemas.StrategyResponse)
def rename_strategy(strategy_id: int, name_data: dict, db: Session = Depends(get_db)):
    db_strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not db_strategy:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    db_strategy.name = name_data.get("name", db_strategy.name)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@app.delete("/api/strategies/{strategy_id}")
def delete_strategy(strategy_id: int, db: Session = Depends(get_db)):
    db_strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not db_strategy:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    db.delete(db_strategy)
    db.commit()
    return {"status": "success"}

@app.post("/api/orchestrate")
async def run_orchestration(context_data: dict, db: Session = Depends(get_db)):
    orchestrator = Orchestrator()
    
    # Initialize shared context from request
    context = SharedContext(
        strategy_name=context_data.get("strategy_name", "Unknown"),
        strategy_code=context_data.get("strategy_code", ""),
        asset=context_data.get("asset", "BTCUSDT"),
        timeframe=context_data.get("timeframe", "1h"),
        parameters=context_data.get("parameters", {}),
        replay_metrics=context_data.get("replay_metrics", {})
    )
    
    # Run the workflow
    final_context = await orchestrator.execute_workflow(context)
    
    return final_context

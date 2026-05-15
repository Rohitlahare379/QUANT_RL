from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TraceEvent(BaseModel):
    agent_id: str
    event_type: str # START, COMPLETE, ERROR, RETRY, TRIGGER
    stage: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    duration_ms: Optional[float] = None
    data: Dict[str, Any] = {}
    message: str

class AgentOutput(BaseModel):
    agent_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str
    data: Dict[str, Any]
    logs: List[str] = []

class SharedContext(BaseModel):
    # Strategy Information
    strategy_id: Optional[int] = None
    strategy_name: str
    strategy_code: str
    
    # Execution Context
    asset: str = "BTCUSDT"
    timeframe: str = "1h"
    parameters: Dict[str, Any] = {}
    
    # Agent Outputs
    regime_analysis: Optional[Dict[str, Any]] = None
    robustness_results: Optional[Dict[str, Any]] = None
    replay_metrics: Optional[Dict[str, Any]] = None
    
    # Workflow State
    current_phase: str = "PENDING"
    agent_outputs: Dict[str, AgentOutput] = {}
    traces: List[TraceEvent] = []
    
    # Final Decision
    deployment_decision: Optional[str] = None # DEPLOY, REJECT, VALIDATION_REQUIRED
    decision_reasoning: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True

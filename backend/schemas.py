from pydantic import BaseModel

class StrategyCreate(BaseModel):
    name: str
    code: str

class StrategyResponse(StrategyCreate):
    id: int

    model_config = {"from_attributes": True}

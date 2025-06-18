from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="strategy_engine")

# simple in-memory store
strategies: Dict[str, Dict] = {}

class IndicatorWeight(BaseModel):
    name: str
    weight: float

class Strategy(BaseModel):
    name: str
    indicators: List[IndicatorWeight]

@app.get("/")
async def root():
    return {"message": "strategy_engine"}

@app.post("/strategy")
async def create_strategy(strategy: Strategy):
    strategies[strategy.name] = strategy.dict()
    return {"status": "created", "strategy": strategy}

@app.get("/strategy/{name}")
async def get_strategy(name: str):
    s = strategies.get(name)
    if not s:
        return {"error": "not found"}
    return s


@app.get("/strategies")
async def list_strategies():
    return {"strategies": list(strategies.values())}

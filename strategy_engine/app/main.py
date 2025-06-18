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
    data = strategy.dict()
    data["enabled"] = False
    strategies[strategy.name] = data
    return {"status": "created", "strategy": data}

@app.get("/strategy/{name}")
async def get_strategy(name: str):
    s = strategies.get(name)
    if not s:
        return {"error": "not found"}
    return s


@app.get("/strategies")
async def list_strategies():
    return {"strategies": list(strategies.values())}


@app.delete("/strategy/{name}")
async def delete_strategy(name: str):
    if name in strategies:
        del strategies[name]
        return {"status": "deleted"}
    return {"error": "not found"}


@app.post("/strategy/{name}/enable")
async def enable_strategy(name: str):
    s = strategies.get(name)
    if not s:
        return {"error": "not found"}
    s["enabled"] = True
    return {"status": "enabled"}


@app.post("/strategy/{name}/disable")
async def disable_strategy(name: str):
    s = strategies.get(name)
    if not s:
        return {"error": "not found"}
    s["enabled"] = False
    return {"status": "disabled"}

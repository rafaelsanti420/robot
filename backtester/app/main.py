from fastapi import FastAPI
from pydantic import BaseModel
import httpx

backtests = {}
backtest_counter = 0

app = FastAPI(title="backtester")

class BacktestRequest(BaseModel):
    symbol: str = "BTCUSDT"
    interval: str = "1m"
    limit: int = 10

@app.get("/")
async def root():
    return {"message": "backtester"}

@app.post("/run")
async def run_backtest(req: BacktestRequest):
    global backtest_counter
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "http://market_data:8000/candles",
            params={"symbol": req.symbol, "interval": req.interval, "limit": req.limit},
        )
        candles = r.json().get("candles", [])
    backtest_counter += 1
    result = {"id": backtest_counter, "candles_used": len(candles)}
    backtests[backtest_counter] = result
    return result


@app.get("/result/{id}")
async def get_result(id: int):
    res = backtests.get(id)
    if not res:
        return {"error": "not found"}
    return res


@app.get("/artifacts/{id}")
async def get_artifacts(id: int):
    if id not in backtests:
        return {"error": "not found"}
    # no real artifacts, return stub paths
    return {"json": f"{id}.json", "plot": f"{id}.png"}

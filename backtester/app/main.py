from fastapi import FastAPI
from pydantic import BaseModel
import httpx

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
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "http://market_data:8000/candles",
            params={"symbol": req.symbol, "interval": req.interval, "limit": req.limit},
        )
        candles = r.json().get("candles", [])
    # extremely simplified backtest: just return candles count
    return {"candles_used": len(candles)}

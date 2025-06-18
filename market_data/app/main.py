from fastapi import FastAPI
from .bybit_connector import BybitConnector

app = FastAPI(title="market_data")
connector = BybitConnector()

@app.get("/")
async def root():
    return {"message": "market_data"}

@app.get("/candles")
async def get_candles(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 10):
    data = await connector.get_latest_candles(symbol, interval, limit)
    return {"candles": data}

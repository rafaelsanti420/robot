import asyncio
from fastapi import FastAPI, WebSocket
from .bybit_connector import BybitConnector

app = FastAPI(title="market_data")
connector = BybitConnector()

available_symbols = ["BTCUSDT", "ETHUSDT"]

@app.get("/")
async def root():
    return {"message": "market_data"}

@app.get("/candles")
async def get_candles(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 10):
    data = await connector.get_latest_candles(symbol, interval, limit)
    return {"candles": data}


@app.websocket("/quotes/ws")
async def quotes_ws(ws: WebSocket, symbol: str = "BTCUSDT"):
    await ws.accept()
    for i in range(3):
        await ws.send_json({"symbol": symbol, "price": 1 + i * 0.1})
        await asyncio.sleep(1)
    await ws.close()


@app.get("/symbols")
async def get_symbols():
    return {"symbols": available_symbols}

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import httpx

app = FastAPI(title="API Gateway")

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

@app.get("/")
async def read_root():
    return {"message": "api_gateway"}

@app.get("/ui")
async def ui():
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.get("/services")
async def service_status():
    services = {
        "indicator_engine": "http://indicator_engine:8000",
        "strategy_engine": "http://strategy_engine:8000",
        "trade_executor": "http://trade_executor:8000",
        "market_data": "http://market_data:8000",
        "backtester": "http://backtester:8000",
    }
    results = {}
    async with httpx.AsyncClient() as client:
        for name, url in services.items():
            try:
                r = await client.get(url)
                results[name] = r.json().get("message")
            except Exception:
                results[name] = "unavailable"
    return results

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text("connected")
    await ws.close()

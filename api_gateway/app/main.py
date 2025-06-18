from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import httpx

from common_lib.auth import create_token

app = FastAPI(title="API Gateway")

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# in-memory stores for this demo
users = {}
external_activity = True
strategies = {}


class UserCreds(BaseModel):
    username: str
    password: str


class ActivityToggle(BaseModel):
    active: bool


class Strategy(BaseModel):
    name: str
    indicators: list

@app.get("/")
async def read_root():
    return {"message": "api_gateway"}


@app.post("/register")
async def register(user: UserCreds):
    if user.username in users:
        raise HTTPException(status_code=400, detail="user exists")
    users[user.username] = user.password
    return {"status": "registered"}


@app.post("/login")
async def login(user: UserCreds):
    if users.get(user.username) != user.password:
        raise HTTPException(status_code=400, detail="invalid credentials")
    token = create_token(user.username)
    return {"token": token}


@app.post("/activity")
async def toggle_activity(toggle: ActivityToggle):
    global external_activity
    external_activity = toggle.active
    return {"active": external_activity}

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


@app.post("/strategies")
async def create_strategy(strategy: Strategy):
    strategies[strategy.name] = {"name": strategy.name, "indicators": strategy.indicators, "active": False}
    return strategies[strategy.name]


@app.get("/strategies")
async def list_strategies():
    return {"strategies": list(strategies.values())}


@app.get("/strategies/{name}")
async def get_strategy(name: str):
    s = strategies.get(name)
    if not s:
        raise HTTPException(status_code=404, detail="not found")
    return s


@app.put("/strategies/{name}")
async def update_strategy(name: str, strategy: Strategy):
    strategies[name] = {"name": strategy.name, "indicators": strategy.indicators, "active": strategies.get(name, {}).get("active", False)}
    return strategies[name]


@app.delete("/strategies/{name}")
async def delete_strategy(name: str):
    if name in strategies:
        del strategies[name]
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="not found")


@app.post("/strategies/{name}/start")
async def start_strategy(name: str):
    s = strategies.get(name)
    if not s:
        raise HTTPException(status_code=404, detail="not found")
    s["active"] = True
    return {"status": "started"}


@app.post("/strategies/{name}/stop")
async def stop_strategy(name: str):
    s = strategies.get(name)
    if not s:
        raise HTTPException(status_code=404, detail="not found")
    s["active"] = False
    return {"status": "stopped"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text("connected")
    await ws.close()

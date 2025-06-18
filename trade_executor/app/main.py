from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="trade_executor")

# simple in-memory toggle
active_trading = False

class Order(BaseModel):
    symbol: str
    side: str  # buy or sell
    qty: float

@app.get("/")
async def root():
    return {"message": "trade_executor"}

@app.post("/toggle")
async def toggle(active: bool):
    global active_trading
    active_trading = active
    return {"active": active_trading}

@app.post("/order")
async def place_order(order: Order):
    if not active_trading:
        return {"status": "inactive"}
    # Mock placing order
    return {"status": "placed", "order": order}

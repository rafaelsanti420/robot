from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="trade_executor")

# simple in-memory toggle
active_trading = False
orders = {}
order_counter = 0

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
    global order_counter
    order_counter += 1
    orders[order_counter] = {"id": order_counter, "order": order.dict(), "status": "placed"}
    return orders[order_counter]


class CancelRequest(BaseModel):
    id: int


@app.post("/order/cancel")
async def cancel_order(req: CancelRequest):
    o = orders.get(req.id)
    if not o:
        return {"status": "not found"}
    o["status"] = "cancelled"
    return {"status": "cancelled", "id": req.id}


@app.get("/orders")
async def list_orders():
    return {"orders": list(orders.values())}

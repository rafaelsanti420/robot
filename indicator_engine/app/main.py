from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="indicator_engine")

class MARequest(BaseModel):
    prices: List[float]
    period: int

@app.get("/")
async def root():
    return {"message": "indicator_engine"}

@app.post("/ma")
async def moving_average(req: MARequest):
    if req.period <= 0 or req.period > len(req.prices):
        return {"error": "invalid period"}
    avg = sum(req.prices[-req.period:]) / req.period
    return {"ma": avg}

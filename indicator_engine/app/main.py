from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI(title="indicator_engine")

class MARequest(BaseModel):
    prices: List[float]
    period: int

class RSIRequest(BaseModel):
    prices: List[float]
    period: int

class EMARequest(BaseModel):
    prices: List[float]
    period: int


class MACDRequest(BaseModel):
    prices: List[float]
    fast: int = 12
    slow: int = 26
    signal: int = 9


class CustomRequest(BaseModel):
    prices: List[float]
    expression: str

@app.get("/")
async def root():
    return {"message": "indicator_engine"}

@app.post("/ma")
async def moving_average(req: MARequest):
    if req.period <= 0 or req.period > len(req.prices):
        return {"error": "invalid period"}
    avg = sum(req.prices[-req.period:]) / req.period
    return {"ma": avg}


@app.post("/rsi")
async def relative_strength_index(req: RSIRequest):
    if req.period <= 0 or req.period >= len(req.prices):
        return {"error": "invalid period"}
    gains = []
    losses = []
    for i in range(1, req.period + 1):
        diff = req.prices[-(req.period + 1) + i] - req.prices[-(req.period + 1) + i - 1]
        if diff >= 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(-diff)
    avg_gain = sum(gains) / req.period
    avg_loss = sum(losses) / req.period
    if avg_loss == 0:
        rsi = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
    return {"rsi": rsi}


@app.post("/ema")
async def exponential_moving_average(req: EMARequest):
    if req.period <= 0 or req.period > len(req.prices):
        return {"error": "invalid period"}
    prices = req.prices
    k = 2 / (req.period + 1)
    ema = sum(prices[:req.period]) / req.period
    for price in prices[req.period:]:
        ema = price * k + ema * (1 - k)
    return {"ema": ema}


@app.post("/macd")
async def macd(req: MACDRequest):
    if req.slow <= req.fast or req.slow > len(req.prices):
        return {"error": "invalid params"}

    def ema(data, period):
        k = 2 / (period + 1)
        ema_val = sum(data[:period]) / period
        for price in data[period:]:
            ema_val = price * k + ema_val * (1 - k)
        return ema_val

    fast_val = ema(req.prices, req.fast)
    slow_val = ema(req.prices, req.slow)
    macd_line = fast_val - slow_val
    signal_line = ema(req.prices[-req.signal - 1 :], req.signal)
    return {"macd": macd_line, "signal": signal_line}


@app.post("/custom")
async def custom_indicator(req: CustomRequest):
    try:
        value = eval(req.expression, {"__builtins__": {}}, {"prices": req.prices})
    except Exception as e:
        return {"error": str(e)}
    return {"value": value}

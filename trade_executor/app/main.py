from fastapi import FastAPI

app = FastAPI(title="trade_executor")

@app.get("/")
async def root():
    return {"message": "trade_executor"}

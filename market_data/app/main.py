from fastapi import FastAPI

app = FastAPI(title="market_data")

@app.get("/")
async def root():
    return {"message": "market_data"}

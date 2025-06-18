from fastapi import FastAPI

app = FastAPI(title="strategy_engine")

@app.get("/")
async def root():
    return {"message": "strategy_engine"}

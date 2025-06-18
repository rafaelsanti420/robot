from fastapi import FastAPI

app = FastAPI(title="backtester")

@app.get("/")
async def root():
    return {"message": "backtester"}

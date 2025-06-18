from fastapi import FastAPI

app = FastAPI(title="indicator_engine")

@app.get("/")
async def root():
    return {"message": "indicator_engine"}

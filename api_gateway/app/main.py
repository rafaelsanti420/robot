from fastapi import FastAPI, WebSocket

app = FastAPI(title="API Gateway")

@app.get("/")
async def read_root():
    return {"message": "api_gateway"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_text("connected")
    await ws.close()

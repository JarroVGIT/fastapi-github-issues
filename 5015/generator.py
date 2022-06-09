from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import uvicorn


app = FastAPI()

@app.websocket("/")
async def ws(websocket: WebSocket):
    await websocket.accept()
    i = 0
    while True:
        try:
            await websocket.send_text(f"Hello - {i}")
            await asyncio.sleep(2)
            i+=1
        except WebSocketDisconnect:
            pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)


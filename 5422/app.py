import asyncio
import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketClose
from websockets.exceptions import ConnectionClosedError

app = FastAPI()


@app.get("/")
async def root():
    return {"hello": "world"}


@app.websocket("/wsx")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        t = datetime.datetime.utcnow().time()
        try:
            if t.second % 5 == 0:
                print("Sending the time!")
                await websocket.send_text(str(t))
                await asyncio.sleep(1)
        except ConnectionClosedError:
            print("Client disconnected.")
            break


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

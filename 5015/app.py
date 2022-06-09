import queue
from typing import Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from asyncio import Queue, Task
import asyncio

import uvicorn
import websockets

class Listener:
    def __init__(self):
        self.subscribers: list[Queue] = []
        self.listener_task: Task
    async def subscribe(self, q: Queue):
        self.subscribers.append(q)

    #this function is for testing, it is called when a certain endpoint is called
    #and is instead of the whole start_listening logic.
    async def receive_and_publish_message(self, msg: Any):
        for q in self.subscribers:
            try:
                q.put_nowait(str(msg))
            except Exception as e:
                raise e

    async def start_listening(self):
        self.listener_task = asyncio.create_task(self._listener())


    async def _listener(self) -> None:
        async with websockets.connect("ws://localhost:8001") as websocket:
            async for message in websocket:
                for q in self.subscribers:
                    await q.put(message)

    async def stop_listening(self):
        if self.listener_task.done():
            self.listener_task.result()
        else:
            self.listener_task.cancel()


global_listener = Listener()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # normally, you would call the start_listener
    # conn = some_method_to_get_postgres_connection()
    # global_listener.start_listening(conn=conn)
    # as i do not have a stream listener, i am passing.
    await global_listener.start_listening()
    return

@app.on_event("shutdown")
async def shutdown_event():
    # Here you would normally call the stop_listener method
    await global_listener.stop_listening()
    return


@app.get('/add_item/{item}')
async def add_item(item: str):
    await global_listener.receive_and_publish_message(item)
    return {"published_message:": item}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    q: asyncio.Queue = asyncio.Queue()
    await global_listener.subscribe(q=q)
    try:
        while True:
            data = await q.get()
            await websocket.send_text(data)
    except WebSocketDisconnect:
            return


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
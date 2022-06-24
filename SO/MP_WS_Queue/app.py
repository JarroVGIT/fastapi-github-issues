import asyncio
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from queue import Empty
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import time

app = FastAPI()

#do not re-create the pool with every request, only create it once
pool = ProcessPoolExecutor()


def long_running_task(q: mp.Queue) -> str:
    # This would be your update_cicada function
    for i in range(5):
        #this represents some blocking IO
        time.sleep(3)
        q.put(f"'result': 'Iteration {i}'")
    return "done!"


@app.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    loop = asyncio.get_event_loop()
    
    #To use Queue's across processes, you need to use the mp.Manager()
    m = mp.Manager()
    q = m.Queue()
    
    await websocket.accept()
    
    #run_in_executor will return a Future object. Normally, you would await
    #such an method but we want a bit more control over it. 
    result = loop.run_in_executor(pool, long_running_task, q)
    while True:
        
        #None of the coroutines called in this block (e.g. send_json()) 
        # will yield back control. asyncio.sleep() does, and so it will allow
        # the event loop to switch context and serve multiple requests 
        # concurrently.
        await asyncio.sleep(0)

        try:
            #see if our long running task has some intermediate result. Will 
            q_result = q.get(block=False)
        except Empty:
            #if q.get() throws Empty exception, then nothing was 
            # available (yet!).
            q_result = None

        #If there is an intermediate result, let's send it to the client.
        if q_result:
            try:
                await websocket.send_json(q_result)
            except WebSocketDisconnect:
                #This happens if client has moved on, we should stop the long
                #  running task
                result.cancel()
                #break out of the while loop.
                break
        
        #We want to stop the connection when the long running task is done.
        if result.done():
            try:
                await websocket.send_json(result.result())
                await websocket.close()  
            except WebSocketDisconnect:
                #This happens if client has moved on, we should stop the long
                #  running task
                result.cancel()
            finally:
                #Make sure we break out of the infinte While loop.
                break
            
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )
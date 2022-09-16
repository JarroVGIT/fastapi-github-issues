import asyncio
import multiprocessing
import random
from concurrent.futures import ProcessPoolExecutor
from threading import Event
from time import sleep, time

from fastapi import FastAPI, Request

app = FastAPI()

# To keep a count of requests, and giving each request a unique ID
app.state.no_requests = 0

# Used to run our long running job in
pool = ProcessPoolExecutor()

# A long running job that we potentially want to terminate
def long_running_blocking(request_id: int, event: Event):
    sleeptime = random.randint(5, 15)
    slept_time = 0
    print(
        f"({request_id}) - Starting long running job, will take {sleeptime} seconds.."
    )

    # Note that this is blocking on purpose to illustrate blocking call.
    while not event.is_set() and slept_time < sleeptime:
        sleep(1)
        slept_time += 1

    if event.is_set():
        print(f"({request_id}) - Terminating long running job.")
        return

    print(f"({request_id}) - Finished long running job.")
    return sleeptime


@app.get("/long")
async def long(request: Request, timeout: int):
    app.state.no_requests += 1
    request_id = request.app.state.no_requests
    print(f"({request_id}) - Received request")

    starttime = time()

    loop = asyncio.get_event_loop()

    # Manager is required to be able to share an Event object between processes
    with multiprocessing.Manager() as manager:
        event = manager.Event()
        fut = loop.run_in_executor(pool, long_running_blocking, request_id, event)

        while (time() - starttime) < timeout:
            if fut.done():
                # If the task is done before the timeout, break out of timeout loop.
                break
            # Try again in 1 second
            await asyncio.sleep(1)

        try:
            result = fut.result()
        except asyncio.InvalidStateError:
            # result() will rase InvalidStateError if the task is not finished.
            event.set()
            result = "Timed out!"
        finally:
            # Allow the running task to handle the event.set() event.
            while not fut.done():
                await asyncio.sleep(0.1)
            # Finally, return the result (either sleeptime or "Timed out!")
            return result


@app.get("/")
async def root():
    return {"hello": "world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

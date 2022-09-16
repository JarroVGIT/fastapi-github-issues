import asyncio
import random
import time

from fastapi import FastAPI, Request

app = FastAPI()

# keep a count of requests, makes reading the log easier.
app.state.request_no = 0


async def get_response_from_external_api(url: str, request_no) -> None:
    # here you would put something like httpx to make async calls to your endpoint.
    # to simulate this takes a while, we will sleep here. And the return value is the
    # url, the time it should take (sleeptime) and the time it did take.
    sleep_time = random.randint(1, 5)
    print(f"({request_no}) Calling {url}, should take {sleep_time} seconds...")
    start = time.time()
    await asyncio.sleep(sleep_time)
    end = time.time()
    print(f"({request_no}) Done calling {url}, took {end-start} seconds...")
    return (url, sleep_time, end - start)


@app.get("/get_response")
async def get_response(r: Request):
    # Using app.state because it will change with every incoming request
    r.app.state.request_no += 1
    request_no = r.app.state.request_no

    # Construct the URLs
    urls = [f"url.com/api/{i}" for i in range(1, 5)]
    print(f"({request_no}) Request has come in.")

    start = time.time()
    result = await asyncio.gather(
        *[get_response_from_external_api(url, request_no) for url in urls]
    )

    end = time.time()
    print(f"({request_no}) Request has been processed.")
    return result


@app.get("/")
async def root():
    return {"hello": "world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

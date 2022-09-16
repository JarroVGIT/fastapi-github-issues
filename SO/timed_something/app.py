from fastapi import FastAPI
import asyncio


class MySharedObject:
    def __init__(self) -> None:
        self.count = 0


async def timed_checker(obj: MySharedObject):
    while True:
        obj.count += 1
        # async with httpx.AsyncClient() as client:
        #    r = await client.get('https://www.example.com/')
        await asyncio.sleep(3)


app = FastAPI()


@app.on_event("startup")
def startup_function():
    app.state.shared_object = MySharedObject()
    asyncio.create_task(timed_checker(app.state.shared_object))


@app.get("/")
async def root():
    return {"hello": "world"}


@app.get("/count")
async def get_count():
    return app.state.shared_object.count


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

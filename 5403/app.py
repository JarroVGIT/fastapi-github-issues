import asyncio
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


async def get_items_from_db():
    print("Get some items from DB..")
    await asyncio.sleep(1)
    return [1, 2, 3, 4]


async def background_task_function():
    print("Background task is executing..")
    result = await get_items_from_db()
    print(f"Items collected: {result}")


@app.get("/")
async def root(bt: BackgroundTasks):
    print("Endpoint is called, now adding BG task..")
    bt.add_task(background_task_function)
    print("BG task added, returning response..")
    return {"hello": "world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

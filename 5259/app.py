from fastapi import Depends, FastAPI, Request, Response
from functools import wraps

app = FastAPI()


def dependency(response: Response):
    print("1. Dependency is called first..")
    response.headers["id"] = "hello"
    print("2. Added a header to the response object, now yield from dependency..")
    yield
    print(
        "4. Any code after yield in the dependency is ran after the response has returned. "
    )


@app.get("/", dependencies=[Depends(dependency)])
async def root():
    print("3. This is executed in your endpoint, after all dependencies have yielded..")
    return {"hello": "world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

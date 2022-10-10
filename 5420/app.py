from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/aaa/{path_params:path}")
async def example(path_params: str = ""):
    return path_params.split("/")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

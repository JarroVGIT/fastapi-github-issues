from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


def some_dependency(param_1: str):
    if param_1 == "error":
        raise HTTPException(400, "Error!!")
    print(param_1)


@app.get("/", dependencies=[Depends(some_dependency)])
async def root(param_1: str):
    return {"oh hi": param_1}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Query, Request

app = FastAPI()


@app.get("/")
async def root(r: Request, event: int | str | None = None, item: int | None = None):
    print(f"Event:{event}.")
    print(f"Item:{item}.")
    print(r.query_params)
    return {"event": event, "item": item}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

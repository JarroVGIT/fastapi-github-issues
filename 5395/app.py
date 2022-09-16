from fastapi import FastAPI, Request

app = FastAPI(title="This is the FastAPI object title")


@app.get("/")
async def root(request: Request):
    return {"app_title": request.app.title}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

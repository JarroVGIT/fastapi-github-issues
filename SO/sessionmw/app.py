import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="some-random-string")


@app.get("/")
async def root(request: Request):
    return request.session


@app.get("/a")
async def session_set(request: Request):
    request.session["my_var"] = "1234"
    return "ok"


@app.get("/b")
async def session_info(request: Request):
    my_var = request.session.get("my_var", None)
    return my_var


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

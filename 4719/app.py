import asyncio
import datetime as dt

import fastapi


async def fake_get_db():
    db = "fake_conn"
    try:
        yield db
    finally:
        print("Before finally await")
        await asyncio.sleep(1)
        print("After finally await")


def get_app():
    app = fastapi.FastAPI()

    @app.middleware("http")
    async def add_process_time_header(request: fastapi.Request, call_next):
        start_time = dt.datetime.now()
        response = await call_next(request)
        process_time = (dt.datetime.now() - start_time).total_seconds()
        response.headers["X-Process-Time"] = str(process_time)
        return response

    @app.get("/test")
    async def test(fake_db: str = fastapi.Depends(fake_get_db)):
        return "OK"

    return app


if __name__ == "__main__":
    import uvicorn

    _app = get_app()
    uvicorn.run(_app, host="0.0.0.0", port=7776)

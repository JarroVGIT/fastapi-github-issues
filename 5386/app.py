from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class Middleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        await request.json()
        response = await call_next(request)
        return response


app = FastAPI()
app.add_middleware(Middleware)


@app.post("/test")
async def test(test: dict) -> dict:
    return {"data": "test"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

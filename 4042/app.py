from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

async def internal_server_error(request: Request, exc: Exception | ValidationError) -> "JSONResponse":
    return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

app = FastAPI(
    exception_handlers={
        Exception: internal_server_error,
        ValidationError: internal_server_error,
    },
)

@app.get("/call_me")
async def raise_exception() -> None:
    raise Exception("I am exception.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104, E261
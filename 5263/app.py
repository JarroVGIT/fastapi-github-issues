from fastapi import FastAPI

# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

# origins = [
#     "http://localhost:5000",
# ]

origins = ""
middleware = [Middleware(CORSMiddleware, allow_origins=origins)]

app = FastAPI(middleware=middleware)
# app = FastAPI()


@app.get("/root")
async def root():
    return {"hello": "world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

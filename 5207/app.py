from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Request, Response, status


ALLOWED_ORIGIN = r"https?:\/\/.*\.example\.(?:com|cloud)"

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_methods=["GET", "PATCH", "POST"], allow_origin_regex=ALLOWED_ORIGIN)


@app.get("/allowed")
async def cors_get():
    return {"message": "GET allowed for /allowed"}


@app.post("/allowed")
async def cors_post():
    return {"message": "POST allowed for /allowed"}


@app.put("/disallowed")
async def cors_put():
    return {"message": "PUT disallowed for /disallowed"}\

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
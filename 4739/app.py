from fastapi.middleware.gzip import GZipMiddleware
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()
app.add_middleware(GZipMiddleware)


@app.get("/receivings")
def receivings() -> StreamingResponse:
    f = open("/Users/jarro/Development/fastapi-github-issues/zelftest/1mb.txt")
    response = StreamingResponse(f, media_type='text/csv')
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, )    
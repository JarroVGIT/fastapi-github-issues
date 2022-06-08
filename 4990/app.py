from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/test")
def test():
    return {'foo': 'bar'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
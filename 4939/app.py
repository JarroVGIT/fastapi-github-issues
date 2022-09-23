import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
async def root():
    raise HTTPException(204)


if __name__ == "__main__":
    uvicorn.run(app, debug=True)

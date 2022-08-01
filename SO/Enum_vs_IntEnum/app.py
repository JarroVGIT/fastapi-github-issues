from enum import Enum, IntEnum
from fastapi import FastAPI


class MyNumber(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3

app = FastAPI()

@app.get("/add/{a:int}/{b:int}")
async def get_model(a: MyNumber, b: MyNumber):

    return {"sum": a + b}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
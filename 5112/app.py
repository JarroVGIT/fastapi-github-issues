from pydantic import BaseModel
from pytest import param
import uvicorn
from fastapi import Depends, FastAPI


class A():
    def __init__(self, param1: str) -> None:
        self.param1 = param1

    def __call__(self, param2: str = "world") -> str:
        return {self.param1: param2}
app = FastAPI()



@app.post("/")
async def root(s = Depends(A("hello"))):
    return s






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104, E261
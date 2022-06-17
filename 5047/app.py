from typing import Optional, Any
from enum import Enum, IntEnum
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app: FastAPI = FastAPI()

class MyEnum(IntEnum):
    STATE_0 = 0
    STATE_1 = 1

class MyCommons(BaseModel):
    state: Optional[MyEnum] = None

@app.get("/")
def get_things(commons: MyCommons = Depends(MyCommons)) -> Any:
    return commons

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, )   
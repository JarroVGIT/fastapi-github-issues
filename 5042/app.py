import typing
from enum import Enum

from fastapi import FastAPI, Query, Depends
from pydantic.dataclasses import dataclass

app = FastAPI()


class Status(str, Enum):
    SUCCESS = "SUCCESS"
    REFUND = "REFUND"
    FAIL = "FAIL"
    CANCEL = "CANCEL"


@app.get("/working-example/")
async def root_with_normal_query_params(status_in: typing.List[Status] = Query(...)):
    return {"status_inputs": status_in}


@dataclass
class StatusModel:
    status_in: list[Status] = Query(...)


@app.get("/not-working-example/")  # it now works
async def root_with_pydantic(status_inputs: StatusModel = Depends()):
    return {"status_inputs": status_inputs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, APIRouter, Depends
import uvicorn
from typing import List
from fastapi import Query
from pydantic import BaseModel, Field
import os


class A(BaseModel):
    foo: str = Query(
        description="This is Foo",
    )


class B(A):
    bar: str = Field(
        description="This is Bar with alias",
        alias="bar2",
    )


class C(B):
    def __init__(self, xyz: str = Query(description="This is Xyz")):
        self.xyz = xyz


app = FastAPI()

rtr_api = APIRouter(prefix="/api")


@rtr_api.get(
    "/test1",
    description="Query me",
    summary="Querio-matic 1",
    response_model=List[B],
)
async def test(bdata: B = Depends()):
    return [bdata]


@rtr_api.get(
    "/test2",
    description="Query me 2",
    summary="Querio-matic 2",
    response_model=List[B],
)
async def test2(bdata: B = Query()):
    return [bdata]


@rtr_api.get(
    "/test3",
    description="Query me 3",
    summary="Querio-matic 3",
    response_model=List[C],
)
async def test3(bdata: C = Depends()):
    return [bdata]


app.include_router(rtr_api)

if __name__ == "__main__":
    uvicorn.run(
        app,
        port=int(os.environ.get("PORT", "8000")),
        host=os.environ.get("HOST", "localhost"),
        debug=True,
    )
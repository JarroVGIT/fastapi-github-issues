from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ResponseModel(BaseModel):
    message: str

app = FastAPI()
router = APIRouter()


@router.get("/a", responses={501: {"description": "Error 1"}})
async def a():
    return "a"


@router.get(
    "/b",
    responses={
        502: {"description": "Error 2"},
        "4XX": {"description": "Error with range, upper"},
    },
)
async def b():
    return "b"


@router.get(
    "/c",
    responses={
        "400": {"description": "Error with str"},
        "5xx": {"description": "Error with range, lower"},
        "default": {"description": "A default response"},
    },
)
async def c():
    return "c"

@router.get(
    "/d",
    responses={
        "400": {"description": "Error with str"},
        "5xx": {"model": ResponseModel},
        "default": {"model": ResponseModel},
    },
)
async def d():
    return "d"

app.include_router(router=router)
# @app.get("/items/{item_id}", responses={200: {"model": Message}, "4XX": {"model": Message}})
# async def read_item(item_id: str):
#     if item_id == "foo":
#         return {"id": "foo", "value": "there goes my hero"}
#     else:
#         return JSONResponse(status_code=404, content={"message": "Item not found"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
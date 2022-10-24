from enum import Enum

from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel

app = FastAPI()


class ShapeModeEnum(str, Enum):
    schematic = "schematic"
    realistic = "realistic"


class ItemBase(BaseModel):
    name: str


class Item(ItemBase):
    shape_mode: ShapeModeEnum

    class Config:
        # allow_mutation = False
        extra = "forbid"
        strict = True
        validate_assignment = True


def get_real_item(request: Request, item: ItemBase) -> Item:
    RESPONSE_CLASSES = {"application/json": "schematic", "image/png": "realistic"}

    return Item(
        name=item.name, shape_mode=RESPONSE_CLASSES[request.headers.get("Accept", None)]
    )


@app.post("/item")
async def get_item(item: Item = Depends(get_real_item)):
    return item


@app.get("/")
async def root():
    return {"hello": "world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

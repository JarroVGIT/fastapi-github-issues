from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class User(BaseModel):
    name: str


class Item(BaseModel):
    size: int
    price: float


app = FastAPI()


@app.post("/multi/")
def process_things(body: Union[User, Item]):
    return body


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

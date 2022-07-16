from typing import Optional, Union
from pydantic import BaseModel, Field

import uvicorn
from fastapi import FastAPI

app = FastAPI()

class NullableResponseModel(BaseModel):
    result: Union[str, None] = Field(None, nullable=True)


@app.get("/someItem", response_model=NullableResponseModel)
async def get_some_item():
    return None

@app.get("/")
async def root():
    return {"message": "Hello World"}





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104, E261
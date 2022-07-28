from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel


DataT = TypeVar("DataT")


class Type(str, Enum):
  green = "green"
  blue = "blue"


class State(str, Enum):
  published = "published"
  archived = "archived"


class FieldFilter(GenericModel, Generic[DataT]):
  eq: Optional[DataT]
  neq: Optional[DataT]

class StringFilter(FieldFilter[str]):
  ilike: Optional[str]
  nilike: Optional[str]

class Where(BaseModel):
  name: Optional[StringFilter]
  # changing either of these lines to FieldFilter[str] resolves the error
  # but obviously we'd like the enums to display in openapi.json rather than str
  type: Optional[FieldFilter[Type]]
  state: Optional[FieldFilter[State]]


class QueryParams(BaseModel):
  where: Optional[Where]
  limit: Optional[int]
  offset: Optional[int]


app = FastAPI()

@app.post("")
def search(params: QueryParams):
    return {"Hello":"Tiangolo"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
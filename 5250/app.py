from typing import Union

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel

ALIAS_NAME = "param-with-alias"


class ParamsWithoutAlias(BaseModel):
    param_without_alias: Union[str, None] = Query(None)


class ParamsWithAlias(BaseModel):
    param_with_alias: Union[str, None] = Query(None, alias=ALIAS_NAME)


app = FastAPI()


@app.get("/api/get")
async def get_route(
    params: ParamsWithoutAlias = Depends(),
    alias_params: ParamsWithAlias = Depends(),
):

    return {}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

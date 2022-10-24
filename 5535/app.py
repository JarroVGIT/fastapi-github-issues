from typing import Union

import uvicorn
from fastapi import APIRouter, Depends, FastAPI, Header, Path, Query
from pydantic import PositiveInt

app = FastAPI()
router = APIRouter()


def get_user_id_from_header(
    user_id_header: Union[PositiveInt, None] = Header(default=None, alias="user_id")
):
    return user_id_header


def get_user_id_from_query(
    user_id_query: Union[PositiveInt, None] = Query(default=None, alias="user_id")
):
    return user_id_query


@router.get("/user/{user_id}")
async def article(
    user_id: PositiveInt = Path(),
    header_user_id=Depends(get_user_id_from_header),
    query_user_id=Depends(get_user_id_from_query),
):
    return {
        "user_id": user_id,
        "header_user_id": header_user_id,
        "query_user_id": query_user_id,
    }


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)

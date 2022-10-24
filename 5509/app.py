from fastapi import Depends, FastAPI, HTTPException, Path
from pydantic import BaseModel, ValidationError

app = FastAPI()


class ListOfIds(BaseModel):
    ids: list[int]


def list_path_param(list_of_ids: str = Path()):
    try:
        ids = ListOfIds(ids=list_of_ids.split(","))
    except ValidationError:
        raise HTTPException(400, "IDs must be valid integers.")
    return ids


@app.get("/controls/{list_of_ids}")
async def get_list_of_ids(list_obj: ListOfIds = Depends(list_path_param)):
    return {"count": len(list_obj.ids), "ids": list_obj.ids}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

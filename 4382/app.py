from typing import Union

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

class responseA(BaseModel):
    name: str

class responseB(BaseModel):
    id: int

app = FastAPI()

@app.get("/", response_model=responseA|responseB )
def base(q: int|str = Query(None)):
    if q and isinstance(q, str):
        return responseA(name=q)
    if q and isinstance(q, int):
        return responseB(id=q)
    raise HTTPException(status_code=400, detail="No q param provided")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )

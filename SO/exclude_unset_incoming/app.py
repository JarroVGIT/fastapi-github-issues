from typing import Union
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Text(BaseModel):
    id: str
    text: str = None


class TextsRequest(BaseModel):
    data: list[Text]
    n_processes: Union[int, None]


@app.get("/")
async def root(req: Request):
    print(req.__dict__)
    return {"hello":"world"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


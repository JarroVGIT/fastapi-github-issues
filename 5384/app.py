from fastapi import Depends, FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    x: str | None = Form()


@app.get("/")
async def foo(item: Item = Depends()):
    print(item.dict(exclude_unset=True, exclude_none=True))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

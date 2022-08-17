from fastapi import FastAPI, Request, Body
from pydantic import BaseModel

app = FastAPI()


# @app.get("/one-random-line")
# async def get_one_random_line(request: Request):
#     # implement your own logic here, this will only return a static line
#     return {"line": "This is an example"}


# @app.get("/one-random-line-backwards")
# async def get_one_random_line_backwards(request: Request):
#     # You don't have to do fancy http stuff, just call your endpoint:
#     one_line = await get_one_random_line(request)
#     return {"line": one_line["line"][::-1]}


# class MyModel(BaseModel):
#     a: str


# @app.get("/")
# async def root(param: MyModel = Body(None)):
#     return "hello world"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

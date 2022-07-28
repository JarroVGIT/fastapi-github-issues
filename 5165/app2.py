from typing import Any
from fastapi import Body, FastAPI, HTTPException, Request, Depends

class RequestModel:
    def __init__(self, r: Request, id: int = Body(), value: Any = Body()) -> None:
        self.id = id
        self.value = value
        if r.state.is_authenticated:
            self.username = r.state.username
        else:
            raise HTTPException(401, "Not Authorized")

app = FastAPI()

@app.middleware("http")
async def add_request_user_to_body(r: Request, call_next):
    #put your JWT logic here, I will just assume you retrieved your username
    r.state.is_authenticated = True
    r.state.username = "user_from_middleware"
    response = await call_next(r)
    return response

@app.post("/test")
async def root(data: RequestModel = Depends() ):
    return {"Hello": data.username, "YourID": data.id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
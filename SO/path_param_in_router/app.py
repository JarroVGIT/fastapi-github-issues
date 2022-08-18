from fastapi import APIRouter, FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"hello": "world"}


router = APIRouter(prefix="/org/{org_id}")


@router.get("/users/{user_id}")
def get_user(org_id: int, user_id: int):
    return {"org": org_id, "user:": user_id}


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

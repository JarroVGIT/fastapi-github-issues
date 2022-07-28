from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

my_router = APIRouter(prefix='/router')


@my_router.get("/not-working")
async def router_root():
    content = "<img src='static/black.png'>"
    # -------------------^ note, not absolute path!
    return HTMLResponse(content=content)

@my_router.get("/working")
async def router_root():
    content = "<img src='/static/black.png'>"
    # -------------------^ note, prefixed slash!
    return HTMLResponse(content=content)

app.include_router(my_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
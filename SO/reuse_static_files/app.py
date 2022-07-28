from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/home', response_class=HTMLResponse)
def home(request: Request):
    return "<link rel='stylesheet' href='/static/test.css'><h1>hello from home</h1>"

router = APIRouter(prefix='/myrouter')

@router.get('/route', response_class=HTMLResponse)
def route(request: Request):
    return "<link rel='stylesheet' href='/static/test.css'><h1>hello from home</h1>"
# ---------------------------------------^ relative path!
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
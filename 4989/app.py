from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/coming_soon/static", StaticFiles(directory="webpages/coming_soon/static"), name="coming_soon_static")


templates = Jinja2Templates(directory="webpages")


@app.get("/coming_soon", response_class=HTMLResponse)
async def coming_soon(request: Request):
    return templates.TemplateResponse("coming_soon/index.html", {"request": request})

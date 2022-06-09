from fastapi import FastAPI

#note: site is a built-in package, so importing it doesn't result in importing site.py..
import site1

site_router = site1.site_route

app = FastAPI()
app.include_router(site_router)

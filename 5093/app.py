from ast import alias
import uvicorn
from fastapi import FastAPI, Depends, Query
from typing import Optional
from pydantic.dataclasses import dataclass
from pydantic import BaseConfig

app = FastAPI()

from pydantic import BaseConfig
BaseConfig.allow_population_by_field_name = True


@dataclass
class Catz:
    qqq: Optional[str] = Query(None, alias='q')

@app.get("/productz/")
def search_products(query: Catz = Depends()):
    products = [{"name": "Computer"}, {"name": "HDD"}]
    if not query.qqq:
        query.qqq = ""
    return {"query": query, "results": [product for product in products if query.qqq in product["name"]]}


@dataclass
class Cats:
    qqq: Optional[str] = Query(None )

@app.get("/products/")
def search_products(query: Cats = Depends()):
    products = [{"name": "Computer"}, {"name": "HDD"}]
    if not query.qqq:
        query.qqq = ""
    return {"query": query, "results": [product for product in products if query.qqq in product["name"]]}

@app.get("/test")
def get_test_query(q: str = Query(None, alias="x")):
    return q


if __name__ == "__main__":
    uvicorn.run("app:app", port=11978, log_level="info", reload=True)
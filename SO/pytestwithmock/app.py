from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import pytest

app = FastAPI()


def do_something():
    return "world"


@app.get("/myroute")
async def myroute():
    try:
        text = do_something()
        return {"hello": text}
    except Exception:
        raise HTTPException(400, "something went wrong")

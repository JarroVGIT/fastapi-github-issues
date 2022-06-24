import asyncio
from typing import AsyncGenerator

import uvicorn
import logging
from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger()


app = FastAPI(debug=True)

class BarMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        logger.warning("BAR: Before call self.app()")
         
        status_code = 1

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                nonlocal status_code
                status_code = message["status"]
            await send(message)
        r = await self.app(scope, receive, send_wrapper)
        logger.warning("BAR: After call self.app()")
        logger.warning(f"BAR: Status code {status_code}")
        logger.warning("BAR: Before sleep()")
        #await asyncio.sleep(2)
        logger.warning("BAR: After sleep()")

class ZxcMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        logger.warning("ZXC: Before call self.app()")
        status_code = 1
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                nonlocal status_code
                status_code = message["status"]
            await send(message)
        r = await self.app(scope, receive, send_wrapper)
        logger.warning("ZXC: After call self.app()")
        logger.warning(f"ZXC: Status code {status_code}")
        logger.warning("ZXC: Before sleep()")
        #await asyncio.sleep(2)
        logger.warning("ZXC: After sleep()")

async def get_foo() -> AsyncGenerator[str, None]:
    logger.warning("BEFORE YIELD FOO")
    yield "foo"
    logger.warning("AFTER YIELD FOO")


async def get_qwerty(foo: str = Depends(get_foo)) -> AsyncGenerator[str, None]:
    logger.warning("BEFORE YIELD QWERTY")
    yield "qwerty"
    logger.warning("AFTER YIELD QWERTY")


app.add_middleware(BarMiddleware)
app.add_middleware(ZxcMiddleware)


@app.get("/")
async def root(qwerty: str = Depends(get_qwerty)):
    return {"message": qwerty}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000,  )
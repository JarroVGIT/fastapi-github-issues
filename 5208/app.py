from fastapi import FastAPI, Request
import typing
import bleach
import json
from starlette.middleware.base import BaseHTTPMiddleware


Scope = typing.MutableMapping[str, typing.Any]
Message = typing.MutableMapping[str, typing.Any]
Receive = typing.Callable[[], typing.Awaitable[Message]]
Send = typing.Callable[[Message], typing.Awaitable[None]]

class SanitizerMiddleware():
    def __init__(self, app) -> None:
        self.app = app

    def __sanitize_array(array_values):
        for index, value in enumerate(array_values):
            if isinstance(value, dict):
                array_values[index] = {key: bleach.clean(
                    value) for key, value in value.items()}
            else:
                array_values[index] = bleach.clean(value)
        return array_values
    
    async def stream(self) -> typing.AsyncGenerator[bytes, None]:
        if hasattr(self, "_body"):
            yield self._body
            yield b""
            return

        if self._stream_consumed:
            raise RuntimeError("Stream consumed")

        self._stream_consumed = True
        while True:
            message = await self._receive()
            if message["type"] == "http.request":
                body = message.get("body", b"")
                if body:
                    yield body
                if not message.get("more_body", False):
                    break
            elif message["type"] == "http.disconnect":
                self._is_disconnected = True
        yield b""
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":  # pragma: no cover
            await self.app(scope, receive, send)
            return
        
        request = Request(scope=scope)
        if request.method in ["POST", "PUT"]:
            json_body = await request.json()
            sanitize_body = {key: self.__sanitize_array(value) if isinstance(
                value, list) else bleach.clean(value) for key, value in json_body.items()}
            request._body = json.dumps(
                sanitize_body, indent=2).encode('utf-8')



class SanitizeMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    @staticmethod
    def __sanitize_array(array_values):
        for index, value in enumerate(array_values):
            if isinstance(value, dict):
                array_values[index] = {key: bleach.clean(
                    value) for key, value in value.items()}
            else:
                array_values[index] = bleach.clean(value)
        return array_values

    async def set_body(self, request: Request):
        receive_ = await request._receive()
        async def receive() -> Message:
            return receive_

        request._receive = receive
        return request

    
    async def dispatch(self, request: Request, call_next):
        await self.set_body(request)

        if request.method == 'POST' or request.method == 'PUT':
            json_body = await request.json()
            sanitize_body = {key: self.__sanitize_array(value) if isinstance(
                value, list) else bleach.clean(value) for key, value in json_body.items()}
            request._body = json.dumps(
                sanitize_body, indent=2).encode('utf-8')
            request = await self.set_body(request)
            request.scope["hello"] = "oh hi mark"
            request.scope['link'] = b'an &lt;script&gt;evil()&lt;/script&gt; example'
        response = await call_next(request)
        return response



app = FastAPI()

app.add_middleware(SanitizeMiddleware)

@app.post("/")
async def root_post(input: dict, request: Request):
    print(request.scope["hello"])
    print(request.scope['link'])
    return input


@app.get("/")
async def root():
    return {"hello":"world"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
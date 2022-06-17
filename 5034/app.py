import typing
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from starlette.background import BackgroundTask
import uvicorn

app = FastAPI()

@app.get("/with_direct_jsonresponse")
async def with_direct_jsonresponse():
    return JSONResponse(content="{'hello':'world']", status_code=408) 
    # 408 will not be documented! Will only show a 200 as per default response class

@app.get("with_direct_jsonresponse_and_responses", 
    responses={406:{"description":"in-line 406 response wut?"}})
async def with_direct_jsonresponse_and_responses():
    return JSONResponse(content="{'hello':'world']") 
    # This would document both 200 (as per default response class) and 406

class CustomJSONResponseWith407(JSONResponse):
    media_type = "application/json"
    def __init__(
        self,
        content: typing.Any,
        status_code: int = 407,
        headers: typing.Optional[dict] = None,
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTask] = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

@app.get("/with_response_class_as_streamingresponse", response_class=StreamingResponse) 
async def with_response_class_as_streamingresponse():
    return {"is this": "a 40x?"}
    # documents only a 407, as the response class is set to that.

@app.get("/with_response_class_and_responses", 
    response_class=CustomJSONResponseWith407, 
    responses={406:{"description":"in-line 406 response wut?"}}) 
async def with_response_class():
    return {"is this": "a 407?"}
    # documents only a 407 as the response class is set to that,
    # But also a 406.


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, )    


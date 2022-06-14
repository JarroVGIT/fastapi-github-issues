from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, Response
import uvicorn

app = FastAPI()


class ImageResponse(Response):
    media_type = "image/*"

    # What do I need to add here to specify that 'format = "binary"'


# here I would like to no longer have to specify 'responses' but only use 'response_class' as a single source of information
@app.post("what_I_currently_do",
    response_class=ImageResponse,
    responses={200: {"content": {
        "image/*": {
            "schema":{
                "type":"string",
                "format": "binary"
            }
        }
    }}},
)
async def send_g(b: UploadFile = File(...)):
    return "/tmp/test/b.jpg"




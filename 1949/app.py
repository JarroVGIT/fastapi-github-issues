from fastapi import FastAPI, UploadFile
from typing import Union

app = FastAPI()


@app.get("/")
async def root():
    return {"hello": "world"}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile] = []):
    if not files:
        return {"message": "Files not attached"}
    else:
        return {"filenames": [file.filename for file in files]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

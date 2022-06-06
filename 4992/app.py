from fastapi import FastAPI,  File, UploadFile
import uvicorn

app = FastAPI()

@app.post("/multi")
async def check_multi_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
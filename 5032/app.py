from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"ok"}

@app.post("/files")
async def files(files: list[UploadFile] | None = None): #The '= None' part makes this an optional parameter!
    return {"message":"ok files"}

@app.post("/file")
async def files(file: bytes | None = File(default=None)): #The '= File(default=None)' part makes this optional
    return {"message":"ok file"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, )    
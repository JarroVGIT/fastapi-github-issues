import aiofiles
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"hello": "world"}


html = """ 
<html>
<head>
    <title>Some Upload Form</title>
    <script src="https://unpkg.com/dropzone@5/dist/min/dropzone.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/dropzone@5/dist/min/dropzone.min.css" type="text/css" />
</head>
<body>
    <form action="/uploadfiles" class="dropzone" id="my-great-dropzone">
    </form>
    <script>
        Dropzone.options.myGreatDropzone = { // camelized version of the `id`
            paramName: "uploaded_files", // The name that will be used to transfer the file
            maxFilesize: 2, // MB
            success: function(file, response){
                console.log(response);
            }
        };
    </script>
    <p id="return-message"></p>
</body>
</html>
"""


@app.get("/form")
async def present_form():
    return HTMLResponse(html)


@app.post("/uploadfiles")
async def create_upload_files(uploaded_files: list[UploadFile]):
    for file in uploaded_files:
        async with aiofiles.open(f"uploaded_files/{file.filename}", "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
        print(f"File uploaded: {file.filename}")
    return {
        "uploaded": [file.filename for file in uploaded_files],
        "random_string": "randomstringhere..",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

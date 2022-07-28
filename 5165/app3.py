from fastapi import FastAPI, Request

app = FastAPI()

@app.get('/api')
@app.get('/api/test')
def main_route(request: Request):
    return {"Called from": request.url.path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
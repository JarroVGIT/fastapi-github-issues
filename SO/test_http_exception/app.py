from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import requests
import anyio

app = FastAPI()

#We've put this in a seperate function so we can mock this.
def get_value():
    return {"msg":"Hello World"}

@app.get('/hello')
async def read_main():
    try:
        print(anyio.to_thread.current_default_thread_limiter().statistics())
        return get_value()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=400,detail='error occured')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
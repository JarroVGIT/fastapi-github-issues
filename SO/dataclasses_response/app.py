import dataclasses
from fastapi import FastAPI

app = FastAPI()

@dataclasses.dataclass
class Response1:
    yo: str

@app.post('/one', response_model=Response1)
def get_responses():
    pass

@app.post('/two', response_model=Response1)  # When I remove this "Response", or I create a second class it works.
def send_responses():
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SomeModel(BaseModel):
    q: dict

@app.post("/query")
def read_query(q: SomeModel):
    return q

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )


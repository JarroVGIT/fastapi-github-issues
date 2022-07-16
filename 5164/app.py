from fastapi import FastAPI
from enum import Enum
app = FastAPI()

class SubType(Enum):
    thriller = "thriller"
    horror = "horror"


@app.get("/{id}-{subId:int}")
async def article_func_b(id: int, subId: int):
    return "show article with subId"

@app.get("/{id}-{subType:str}")
async def article_func_a(id: int, subType: SubType):
    return "show article with subtype"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )

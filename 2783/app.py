from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BaseClass(BaseModel):
    id: int
    name: str

class SubclassA(BaseClass):
    level: str
    previous_level: str

class SubclassB(BaseClass):
    email: str
    subject: str
    

class SubclassC(BaseClass):
    level: str
    previous_level: str | None
   

class SubclassD(BaseClass):
    level: str
    next_level: str
    

@app.get('/test', response_model=list[SubclassA|SubclassB|SubclassC|SubclassD])
async def get_classes():
    result = [SubclassC(id=1, level="level", name="name", previous_level=None), SubclassA(id=2, level="level", name='name', previous_level='prev')]
    return result

@app.get("/")
async def root():
    return {"hello":"world"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
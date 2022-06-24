from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

    


class MyBaseModel(BaseModel):
    pass

    class Config:
        json_encoders = {
            ObjectId: lambda oid: str(oid)
        }


class Model2(MyBaseModel):
    a: PyObjectId


class Model1(MyBaseModel):
    a: str = Field(example="Foo")
    b: Model2 = Field(example={"a":"62960507a3f31888572152e2"})


app = FastAPI()


@app.get("/", response_model=Model1)
def read_root():
    model2 = Model2(
        a="62960507a3f31888572152e2"
    )
    model1 = Model1(
        a="Fii",
        b=model2
    )
    return model1

@app.get("/path")
def read_path(input: Model1):
    return input
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )
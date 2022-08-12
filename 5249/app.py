from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


@app.post("/one_body")
def one_body(sentence_1: str = Body(default=None, example="This should works fine")):
    return "'I'm one_body"


@app.post("/only_body")
def only_body(
    sentence_1: str = Body(default=None, example="some example value (1)"),
    sentence_2: str = Body(default=None, example="some example value (2)"),
):
    return "'I'm only_body"


class Sentence1(BaseModel):
    sentence_1: str

    class Config:
        schema_extra = {
            "example": "This is the first sentence that I have hard-coded",
        }


class Sentence2(BaseModel):
    sentence_2: str

    class Config:
        schema_extra = {
            "example": "This is the second sentence that I have hard-coded",
        }


class Sentence3(BaseModel):
    sentence_1: str
    sentence_2: str

    class Config:
        schema_extra = {
            "examples": [
                {
                    "sentence_1": "Hello sentence 1 from model3",
                    "sentence_2": "Hello sentence 2 from model3",
                },
            ]
        }


@app.post("/with_base_model")
def with_base_model(sentence_1: Sentence1, sentence_2: Sentence2):
    return "'I'm only_body"


@app.post("/with_model_3")
def with_model_3(sentences: Sentence3):
    return "hello there"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

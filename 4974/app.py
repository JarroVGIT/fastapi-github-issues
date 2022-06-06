from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.param_functions import Depends
from pydantic import BaseModel, ValidationError
from pydantic.class_validators import root_validator, validator
import uvicorn

app = FastAPI()


class Options(BaseModel):
    a: Optional[int]
    b: Optional[int]

    @root_validator() 
    def at_least_one_option(cls, values):
        try:
            assert any(
                opt is not None for opt in values.values()
            ), "At least one option should be enabled."
        except:
            raise HTTPException(status_code=422, detail="Hallo!!")
        return values


@app.get("/")
def read_root(options: Options = Depends(Options)):
    return options


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
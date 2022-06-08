from decimal import Decimal
from typing import Any
import uvicorn
import simplejson
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class ModelWithDecimal(BaseModel):
    foo: Decimal
    
    class Config:
        json_encoders = {
            Decimal: lambda a: a
        }

class MyJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        print("MyJSONResponse is called")
        v = simplejson.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            use_decimal=True,
        ).encode("utf-8")
        return v

app = FastAPI(default_response_class=MyJSONResponse)

pi_model = ModelWithDecimal(foo=Decimal("3.14159265358979323846264338327950288"))


@app.get("/implicit", response_model=ModelWithDecimal)
def implicit():
    return pi_model


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
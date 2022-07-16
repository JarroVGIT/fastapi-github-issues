from dataclasses import dataclass
from typing import Dict

import uvicorn
from fastapi import FastAPI, status


@dataclass
class A:
    a: int


@dataclass
class B:
    a: A
    b: Dict[str, A]


app = FastAPI()


@app.get("/", responses={
    status.HTTP_200_OK: {
        "model": B,
        "description": "Some B"
    }
})
def foo() -> B:
    return B(
        a=A(1),
        b={"foo": A(2)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104, E261

# This code is complete, run as-is
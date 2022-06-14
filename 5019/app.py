from pydantic import BaseModel, Field
from fastapi import Path, FastAPI, Depends
import uvicorn

app = FastAPI()

class Foo(BaseModel):
    bar: str = Path('bar')  # default value is defined

def get_foo():
    return Foo()
@app.get('/foo')  # always will return 422 because `bar` not represent in path
def pathless_handler(params: Foo = Depends(Foo)):     
    pass

@app.get('/foo/{bar}')
def path_aware_handler(params: Foo = Depends(Foo)):
    pass

@app.get('/wo')
def without_foo_class(params: Foo=Depends(get_foo)):
    print(params)
    return params

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, )    
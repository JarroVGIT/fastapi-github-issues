from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.dependencies.models import Dependant
from pydantic import BaseModel

app = FastAPI()


def get_query_param_from_dependancy(dependant: Dependant):
    params = []
    if dependant.dependencies:
        for dependancy in dependant.dependencies:
            params.extend(get_query_param_from_dependancy(dependancy))
    return params.extend(
        [
            param.alias
            for dependency in dependant.dependencies
            for param in dependency.query_params
        ]
    )


def strict_query_params(request: Request):
    app: FastAPI = request.app
    requested_path = request.scope["path"]
    dependant: Dependant = request.scope["route"].dependant
    allowed_params = get_query_param_from_dependancy(dependant)
    for requested_param, param_value in request.query_params.items():
        if requested_param not in allowed_params:
            raise HTTPException(
                400, f"Not allowed param: {requested_param}: {param_value}"
            )
    return


class OtherParams(BaseModel):
    param4: str | None = Query(None)


class MyParams(BaseModel):
    param1: str | None = Query(None)
    param2: str | None = Query(None)


@app.get("/")
def root(*, params: MyParams = Depends(), _=Depends(strict_query_params)):
    if params.param1:
        return {"param1": params.param1}
    return {"hello": "world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

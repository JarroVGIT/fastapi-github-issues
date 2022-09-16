from copy import deepcopy
from fastapi import FastAPI, Path, Query
from fastapi.openapi.utils import get_openapi
import re

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema_for_iteration = deepcopy(openapi_schema)
    openapi_schema["paths"] = {}

    for path, path_definition in schema_for_iteration["paths"].items():
        list_of_path_params_with_underscores = re.findall("{([a-zA-Z_]*)}", path)
        if list_of_path_params_with_underscores:
            # Change the 'path' key and replace _ with -
            new_path = path.replace("_", "-")
            openapi_schema["paths"][new_path] = schema_for_iteration["paths"][path]
            # For each path param with underscores, changes the parameter name
            for path_param in list_of_path_params_with_underscores:
                new_path_param = path_param.replace("_", "-")
                for http_verb, http_verb_definition in path_definition.items():
                    for index, param in enumerate(http_verb_definition["parameters"]):
                        if param["name"] == path_param:
                            openapi_schema["paths"][new_path][http_verb]["parameters"][
                                index
                            ]["name"] = new_path_param
        else:
            # If there are no path params with underscores, take the original definition
            openapi_schema["paths"][path] = schema_for_iteration["paths"][path]

    return openapi_schema


app.openapi = custom_openapi


@app.get("/{my_id}/list")
def list_items(my_id: str = Path()):
    return {"id": my_id}


@app.get("/query")
def query_param(other_query: str = Query(alias="other-query")):
    return {"q": query_param}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

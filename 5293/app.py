from collections import defaultdict

from fastapi import FastAPI, Query

app = FastAPI()


def cat(url: str):
    return {"message": "category"}


def rep(url: str):
    return {"message": "Reputation"}


def topcat(url: str):
    return {"message": "Top Category"}


mapping = {"cat": cat, "rep": rep, "topcat": topcat}


@app.get("/urlinfo/{to_include:path}")
def get_urlinfo(to_include: str, url: str = Query(None)):
    kinds = set(to_include.strip("/").split("/"))
    responses = defaultdict(list)
    for kind in kinds:
        func = mapping.get(kind, None)
        if func:
            for key, value in (func(url)).items():
                responses[key].append(value)
    return responses


@app.get("/")
async def root():
    return {"hello": "world"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

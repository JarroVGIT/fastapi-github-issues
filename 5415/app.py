from pprint import pprint as pp

import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, Request
from pydantic import BaseModel, Field, ValidationError

app = FastAPI()


class MetadataOut(BaseModel):
    """
    Model for Metadata
    """

    region: str = Field(
        ...,
        title="region",
        description="region - one of dc00|dc01|dc02",
        regex=r"^(dc00|dc01|dc02)$",
    )


@app.get("/api/v1/metadata/fail", response_model=MetadataOut)
def metadatafail():
    return {"region": "whoops"}


@app.get("/api/v1/metadata/failwitherror", response_model=MetadataOut)
def metadatafailwitherror():
    try:
        return MetadataOut(region="whoops")
    except ValidationError as e:
        pp(e)
        raise HTTPException(status_code=422, detail=e.errors())


@app.get("/api/v1/metadata/pass", response_model=MetadataOut)
def metadatapass():
    return {"region": "dc01"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

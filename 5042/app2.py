
from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from enum import Enum

app = FastAPI()

#----------------------------------------------
class Status(Enum):
    SUCCESS = "SUCCESS"
    REFUND = "REFUND"
    FAIL = "FAIL"
    CANCEL = "CANCEL"

#class with list of Enum:
class StatusModelWithListEnum(BaseModel):
    status_in: list[Status] = Query()

#class with Enum:
class StatusModelNoList(BaseModel):
    status_in: Status = Query(...)

#class with list of str:
class OtherModelWithListStr(BaseModel):
    some_param: list[str] = Query(...)

#class with str:
class OtherModelNoList(BaseModel):
    some_param: list[str] = Query(...)


#----------------------------------------------
#The following 4 endpoints do not show correctly in the docs, 
#as they are referencing pydantic models.
@app.get("/statusmodel-list")
async def statusmodel_list(par: StatusModelWithListEnum = Depends()):
    return {"status_inputs": par}
    #shows as request body.

@app.get("/statusmodel-nolist")
async def statusmodel_nolist(par: StatusModelNoList = Depends()):
    return {"status_inputs": par}
    #shows as query

@app.get("/stringmodel-list")
async def stringmodel_list(par: OtherModelWithListStr = Depends()):
    return {"status_inputs": par}
    #shows as request body

@app.get("/stringmodel-nolist")
async def stringmodel_nolist(par: StatusModelNoList = Depends()):
    return {"status_inputs": par}
    #shows as query

@app.get("/no-model-string-list")
async def no_model_string_list(par: list[str] = Query()):
    return {"status_inputs": par}
    #as per docs, shows as query!


#----------------------------------------------
#The following endpoint will show correctly.
@app.get("/status-list-direct-in-param")
async def status_list_in_param(par: list[Status] = Query()):
    return {"status_inputs": par}

@app.get("/status-nolist")
async def stringmodel_nolist(par: Status = Query()):
    return {"status_inputs": par}

@dataclass
class StatusModel:
    status_in: list[Status] = Query(...)

@app.get("/example-with-dataclass/")  # it now works
async def root_with_pydantic(status_inputs: StatusModel = Depends()):
    return {"status_inputs": status_inputs}

#----------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, )    
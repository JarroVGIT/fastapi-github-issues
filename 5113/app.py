from tabnanny import check
from typing import Any, Callable
from fastapi import FastAPI, Depends, HTTPException, Request
from functools import partial
app = FastAPI()

#note, this cannot be a class. Classes that are dependencies are initiated on startup, 
#so you can't pass the request object (as that is not available, at startup).

def checkPerms(or_classes: list[list[Callable | str]], request: Request) -> bool:
    result = []
    #let's call all subclasses
    for cls in or_classes:
        #check if there are arguments
        if len(cls) > 1:
            c = cls[0]()
            res = c(*cls[1::], request)
        else:
            #else call the class directly without arguments.
            c = cls[0]()
            res = c(request)
        if isinstance(res, bool):
            result.append(res)
        else:
            raise HTTPException(detail="Authentication did not return bool")
        #return if any of the results is True.
    return sum(result) > 0

class IsAdmin:
    def __init__(self) -> None:
        return

    def __call__(self, request: Request) -> bool:
        #simulation: if there is a ?q=whatever present in the url, this will return True.
        if request.query_params.get("q"):
            return True
        return False

class HasPerm:
    def __init__(self) -> None:
        return

    def __call__(self, permission: str, request: Request) -> bool:
        #just some logic, to illustrate how it works with params.
        if not permission:
            return False
        if permission == "read":
            return True
        if permission == "write":
            return False

checkperms_admin_write = partial(checkPerms, [[IsAdmin], [HasPerm, "write"]])
checkperms_admin_read = partial(checkPerms, [[IsAdmin], [HasPerm, "read"]])
@app.get("/with-write-perm")
async def with_write(perms:bool = Depends(checkperms_admin_write)):
    #returns false without ?q= in url
    return perms
    
@app.get("/with-read-perm")
async def with_read(perms:bool = Depends(checkperms_admin_read)):
    return perms


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )
from fastapi import FastAPI, HTTPException, Request, Depends

async def username_dependency(r: Request):
    #put your JWT logic here, I will just assume you retrieved your username
    r.state.is_authenticated_from_dependency = True
    r.state.username_from_dependency = "user_from_dependency"
    return

app = FastAPI(dependencies=[Depends(username_dependency)])

# @app.middleware("http")
# async def add_request_user_to_body(r: Request, call_next):
#     #put your JWT logic here, I will just assume you retrieved your username
#     r.state.is_authenticated_from_mw= True
#     r.state.username_from_mw = "user_from_middleware"
#     response = await call_next(r)
#     return response

@app.get("/from_dependency")
async def root(r: Request):
    if r.state.is_authenticated_from_dependency:
        return r.state.username_from_dependency
    return HTTPException(401, "You are not authenticated!")

# @app.get("/from_middleware")
# async def root(r: Request):
#     if r.state.is_authenticated_from_mw:
#         return r.state.username_from_mw
#     return HTTPException(401, "You are not authenticated!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
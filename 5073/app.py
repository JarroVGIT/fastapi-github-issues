from fastapi import FastAPI, HTTPException

class CustomMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        if "/user/" in (scope["path"]).lower():
            print("user should be authenticated, path: ", scope["path"])
            user_is_authenticated = False #replace with your logic.
            if user_is_authenticated:
                r = await self.app(scope, receive, send)
                r
            else:
                #note, this wouldn't work and will result in a 500 internal server error.
                #raise HTTPException(401, "Not Authenthicated!")
                print("user not auththenticated")
                pass
        else:
            #unauthenticated endpoints:
            print("no need for authentication, path: ", scope["path"])
            await self.app(scope, receive, send)


app = FastAPI()

app.add_middleware(CustomMiddleware)


@app.get("/some_endpoint")
async def some_endpoint():
    return "hello"

@app.get("/some_other_endpoint")
async def some_other_endpoint():
    return "hello"

@app.get("/user/authenticated_endpoint")
async def user_authenticated_endpoint():
    return "hello"

@app.get("/user/other_authenticated_endpoint")
async def user_other_authenticated_endpoint():
    return "hello"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )
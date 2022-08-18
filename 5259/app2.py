    from typing import Any, Callable

    from fastapi import APIRouter, Depends, FastAPI, Response

    app = FastAPI()


    class MyCommonDependencyClass:
        def __init__(self, dependency_func: Callable[..., Any] = None) -> None:
            self.dependency_func = dependency_func

        def __call__(self, response: Response) -> Any:
            print("this is from the common dependency class")
            self.dependency_func(response)


    def dependency_function_for_router_1(response: Response):
        print("this is from dependency_function_for_router_1")
        response.headers["hello"] = "world1"


    def dependency_function_for_router_2(response: Response):
        print("this is from dependency_function_for_router_2")
        response.headers["hello"] = "world2"


    @app.get("/")
    async def root():
        return {"hello": "world"}


    dependency_for_router_1 = MyCommonDependencyClass(dependency_function_for_router_1)
    router1 = APIRouter(prefix="/router1")


    @router1.get("/", dependencies=[Depends(dependency_for_router_1)])
    async def from_router1():
        return "hello world1"


    dependency_for_router_2 = MyCommonDependencyClass(dependency_function_for_router_2)
    router2 = APIRouter(prefix="/router2")


    @router2.get("/", dependencies=[Depends(dependency_for_router_2)])
    async def from_router2():
        return "hello world2"


    app.include_router(router1)
    app.include_router(router2)

    if __name__ == "__main__":
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8000)

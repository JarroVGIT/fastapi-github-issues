import fastapi
import fastapi.exception_handlers
import fastapi.testclient
import starlette.exceptions

app = fastapi.FastAPI(root_path="/api", title="Custom root path problem")
router = fastapi.APIRouter(prefix="/api")


@app.exception_handler(starlette.exceptions.HTTPException)
async def http_handler(request: fastapi.Request, exception: fastapi.HTTPException):
    print("HTTP error: ", exception.detail, "; URL in the request object:", request.url)
    response = await fastapi.exception_handlers.http_exception_handler(
        request, exception
    )
    return response


@app.exception_handler(Exception)
async def exception_handler(request: fastapi.Request, exception: Exception):
    print("Exception", exception, "; URL in the request object:", request.url)
    return fastapi.responses.PlainTextResponse(str(exception), status_code=500)


@router.get("/abc")
def abc_handler():
    raise Exception("Error in ABC")


@router.get("/xyz")
def xyz_handler(request: fastapi.Request):
    print("URL in the request-as-argument:", request.url)
    return "XYZ"


app.include_router(router)


if __name__ == "__main__":
    client = fastapi.testclient.TestClient(app)
    print("Test 1: request-as-argument vs response.request")

    url = "/api/xyz"
    response = client.get(url)
    print("URL in response.request:", response.request.url)

    print("Test 2: expected/not expected errors")

    print("Test 2.1:")
    url = "/abc"
    print("Requesting", url, "; NotFound is expected because the url is wrong")
    try:
        client.get(url)
    except Exception:
        print("Exception is caught")

    print("Test 2.1:")
    url = "/api/abc"
    print("Requesting", url, "; Exception is expected because the url is right")
    try:
        client.get(url)
    except Exception:
        print("Exception is caught")

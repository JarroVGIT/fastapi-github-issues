from fastapi import Depends
from custom_fastapi import CustomFastAPI as FastAPI

app = FastAPI()
subapp = FastAPI(dependency_overrides_provider=app)


def get_value():
    return "abc"


@subapp.get("/")
async def index(value: str = Depends(get_value)):
    return "value: " + value

app.mount("/sub", subapp)
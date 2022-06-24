from fastapi import FastAPI
from pydantic import BaseModel, IPvAnyAddress
import aiohttp
app = FastAPI()



@app.get("/check/ip", tags=["Country Check"])
async def get_by_ip(requested_ip: IPvAnyAddress):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://externalapi.com/ip?={requested_ip}") as response:
            json_response = await response.json()
            return_value = {}
            return_value["status"] = response.json()
            return 


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, )    

    
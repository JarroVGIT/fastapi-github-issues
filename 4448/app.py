from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/items")
async def read_item(item_id: str):
    if True:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": "hoi"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

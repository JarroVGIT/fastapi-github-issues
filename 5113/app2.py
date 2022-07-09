from fastapi import FastAPI, Depends, HTTPException, Request

app = FastAPI()

class A:
    def __init__(self, req: Request) -> None:
        return True


@app.get("/")
def root(a = Depends(A)):
    return a

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )
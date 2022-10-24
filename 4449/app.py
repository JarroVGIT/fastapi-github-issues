from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
async def root():
    return {"hello": "world"}


# @app.get("/{job_event_id:path}")
# async def get_all_or_one_event(job_event_id):
#     params = job_event_id.split("/")
#     if len(params) > 2:
#         raise HTTPException(400, "To many params.")
#     elif len(params) == 2:
#         return get_one_event(params[0], params[1])
#     else:
#         return get_all_events(params[0])


def get_all_events(job_id: str):
    return f"All events of job {job_id}!"


def get_one_event(job_id: str, event_id: str):
    return f"Event {event_id} of job {job_id}!"


@app.get("/test/{job_id}/{event_id}")
async def one_or_more_events(job_id: str, event_id: str | None):
    if not event_id:
        return get_all_events(job_id)
    else:
        return get_one_event(job_id, event_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import io

import pandas as pd

app = FastAPI(redirect_slashes=False)

@app.get("/plain_text")
async def plain_text():
    f = io.StringIO()
    url = 'https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/official_datasets/can/phac_n_tests_performed_timeseries_prov.csv'
    df = pd.read_csv(url, index_col=0)
    df.to_csv(f, index=False)
    # print(f.getvalue())
    return StreamingResponse(iter([f.read().encode('utf-8')]), media_type="text/csv")

@app.get("/test")
async def test(r: Request):
    return "hi"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )
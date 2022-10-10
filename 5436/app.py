from decimal import Decimal, getcontext, localcontext
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, condecimal, validator

app = FastAPI()


class DiscountItem(BaseModel):
    name: Optional[str] = None
    total: condecimal(decimal_places=4)


class DiscountItem2(BaseModel):
    name: Optional[str] = None
    total: Decimal

    @validator("total", pre=True)
    def make_four_digits(cls, v):
        getcontext().prec = 4
        v = Decimal(value=v) * Decimal(1)
        # Note that contect precision is only used in aritmethic
        # operations and not when constructing a Decimal
        return v


@app.get("/dec")
async def dec():
    item = DiscountItem2(name="ItemName", total=1.123456789)
    return item


@app.get("/")
async def root():
    total = 0.00012
    item = DiscountItem(name="ItemName", total=0.00012)
    return item


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

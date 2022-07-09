from fastapi import FastAPI, Response

app = FastAPI()

response_examples = {
    200: {
        "description": "Success",
        "content": {
            "application/xml": {
                "example": {
                    """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
                }
            }
        },
    },
    400: {"description": "An invalid value for header content-type."},
    405: {"description": "Endpoint only supports POST."},
    500: {"description": "Internal server error."},
}

class XMLResponse(Response):
    media_type = "application/xml"



@app.get("/legacy/", responses=response_examples, response_class=XMLResponse)
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return XMLResponse(content=data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,  )
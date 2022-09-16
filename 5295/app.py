from fastapi import Depends, FastAPI, Request

app = FastAPI()


def get_images_from_db():
    return [
        {"id": 1, "image_url": "./static/image_name1.png"},
        {"id": 2, "image_url": "./static/image_name2.png"},
    ]


@app.get("/get/image")
async def get_image(
    request: Request, img: list[dict[str, int | str]] = Depends(get_images_from_db)
):
    for img_obj in img:
        img_obj["image_url"] = str(request.base_url) + img_obj["image_url"][2:]
    return img


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)

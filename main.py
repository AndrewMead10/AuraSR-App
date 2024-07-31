import io
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from PIL import Image
from aura_sr import AuraSR
import uvicorn

from fasthtml import FastHTML
from fasthtml.common import *

app = FastHTML()

aura_sr = None


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upscale")
async def upscale_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    upscaled_image = aura_sr.upscale_4x_overlapped(image)

    img_byte_arr = io.BytesIO()
    upscaled_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2345, reload=True)

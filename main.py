from fasthtml import FastHTML, picolink
from fasthtml.common import *
from aura_sr import AuraSR
from PIL import Image
import io
import base64
import time

aura_sr = None


def on_startup(app):
    global aura_sr
    aura_sr = AuraSR.from_pretrained("fal/AuraSR-v2")
    yield


app = FastHTML(
    hdrs=(
        picolink,
        Link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/img-comparison-slider@8/dist/styles.css",
        ),
        Script(
            src="https://cdn.jsdelivr.net/npm/img-comparison-slider@8/dist/index.js"
        ),
        Style(
            """
        :root {
            --primary: #007bff;
            --primary-hover: #0056b3;
        }
        body { background-color: #1a1a1a; color: #ffffff; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .title { text-align: center; margin-bottom: 20px; }
        .input-bar { display: flex; justify-content: space-between; margin-bottom: 20px; }
        .image-container { position: relative; max-width: 100%; height: calc(100vh - 200px); display: flex; justify-content: center; align-items: center; }
        .image-container img { max-width: 100%; max-height: 100%; object-fit: contain; }
        .spinner { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
        .hidden { display: none; }
        #submit-btn, #download-btn { padding: 10px 20px; background-color: var(--primary); color: white; border: none; cursor: pointer; transition: background-color 0.3s; }
        #submit-btn:hover, #download-btn:hover { background-color: var(--primary-hover); }
        #submit-btn:disabled { background-color: #cccccc; cursor: not-allowed; }
        #upscale-time { text-align: center; margin-top: 10px; }
    """
        ),
    ),
    lifespan=on_startup,
)


def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


@app.get("/")
def home():
    return (
        Title("AuraSR Upscaler"),
        Main(
            H1("AuraSR Upscaler", cls="title"),
            Div(
                Input(type="file", id="image-input", accept="image/*"),
                Button("Submit", id="submit-btn", disabled=True),
                Button("Download", id="download-btn", cls="hidden"),
                cls="input-bar",
            ),
            Div(id="image-container", cls="image-container"),
            Div(id="upscale-time", cls="hidden"),
            cls="container",
        ),
        Script(
            """
            const imageInput = document.getElementById('image-input');
            const submitBtn = document.getElementById('submit-btn');
            const downloadBtn = document.getElementById('download-btn');
            const imageContainer = document.getElementById('image-container');
            const upscaleTimeDiv = document.getElementById('upscale-time');
            let upscaledImageData = null;
            
            imageInput.addEventListener('change', () => {
                submitBtn.disabled = !imageInput.files.length;
                if (imageInput.files.length) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        imageContainer.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image">`;
                    };
                    reader.readAsDataURL(imageInput.files[0]);
                }
            });
            
            submitBtn.addEventListener('click', async () => {
                const formData = new FormData();
                formData.append('image', imageInput.files[0]);
                
                imageContainer.innerHTML += '<div class="spinner">Loading...</div>';
                upscaleTimeDiv.classList.add('hidden');
                
                const startTime = Date.now();
                const response = await fetch('/upscale', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                const endTime = Date.now();
                
                imageContainer.innerHTML = `
                    <img-comparison-slider>
                        <img slot="first" src="data:image/png;base64,${result.original}" alt="Original">
                        <img slot="second" src="data:image/png;base64,${result.upscaled}" alt="Upscaled">
                    </img-comparison-slider>
                `;
                
                upscaledImageData = result.upscaled;
                downloadBtn.classList.remove('hidden');
                
                const totalTime = (endTime - startTime) / 1000;  // Convert to seconds
                const serverTime = result.upscale_time;
                upscaleTimeDiv.innerHTML = `Total time: ${totalTime.toFixed(2)}s (Server processing: ${serverTime.toFixed(2)}s)`;
                upscaleTimeDiv.classList.remove('hidden');
            });
            
            downloadBtn.addEventListener('click', () => {
                if (upscaledImageData) {
                    const link = document.createElement('a');
                    link.href = `data:image/png;base64,${upscaledImageData}`;
                    link.download = 'upscaled_image.png';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }
            });
        """
        ),
    )


@app.post("/upscale")
async def upscale(request):
    form = await request.form()
    image = Image.open(form["image"].file)

    start_time = time.time()
    upscaled_image = aura_sr.upscale_4x_overlapped(image)
    end_time = time.time()

    upscale_time = end_time - start_time

    return {
        "original": encode_image(image),
        "upscaled": encode_image(upscaled_image),
        "upscale_time": upscale_time,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=2345, reload=True)

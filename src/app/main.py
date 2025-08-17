import datetime
import uuid

from config import *
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services import ImageClassifier

image_classifier = ImageClassifier()

app = FastAPI()


templates = Jinja2Templates(directory=BASE_DIR / TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=BASE_DIR / STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=BASE_DIR / UPLOADS_DIR), name="uploads")
app.mount(
    "/processed", StaticFiles(directory=BASE_DIR / PROCESSED_DIR), name="processed"
)


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Returning the start page"""
    return templates.TemplateResponse(
        "index.html", {"request": request, "current_time": datetime.datetime.now()}
    )


async def process_uploaded_image(image: UploadFile) -> list:
    """Processes the uploaded image and returns the URL of the processed file"""

    file_ext = image.filename.split(".")[-1]  # type: ignore
    filename = f"{uuid.uuid4()}.{file_ext}"
    input_path = os.path.join(BASE_DIR / UPLOADS_DIR, filename)

    # Saving the original image
    with open(input_path, "wb") as buffer:
        buffer.write(await image.read())

    # Image Processing
    processed_filename = f"processed_{filename}"
    output_path = os.path.join(BASE_DIR / PROCESSED_DIR, processed_filename)
    list_found_objects = image_classifier.classification_process(
        input_path, output_path
    )

    return [f"processed/{processed_filename}", list_found_objects]


@app.post("/upload")
async def upload_image(request: Request, image: UploadFile = File(...)):
    """Processing of the uploaded image (HTML response)"""
    processed_url = await process_uploaded_image(image)
    return templates.TemplateResponse(
        "processed_image.html",
        {"request": request, "processed_image": processed_url[0]},
    )


@app.post("/api/upload")
async def api_upload_image(request: Request, image: UploadFile = File(...)):
    """Processing of the uploaded image (endpoint API)"""
    processed_url, list_found_objects = await process_uploaded_image(image)

    return {
        "status": "success",
        "processed_image": processed_url,
        "count_found_objects": len(list_found_objects),
        "predictions": list_found_objects
    }

import datetime
import os
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services import ImageClassifier

image_classifier = ImageClassifier()

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
UPLOADS_DIR = "uploads"
PROCESSED_DIR = "processed"

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

templates = Jinja2Templates(directory=BASE_DIR / TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=BASE_DIR / STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=BASE_DIR / UPLOADS_DIR), name="uploads")
app.mount("/processed", StaticFiles(directory=BASE_DIR / PROCESSED_DIR), name="processed")



@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Returning the start page"""
    return templates.TemplateResponse(
        "index.html", {"request": request, "current_time": datetime.datetime.now()}
    )


@app.post("/upload")
async def upload_image(request: Request, image: UploadFile = File(...)):
    """Processing the uploaded image"""

    file_ext = image.filename.split(".")[-1] # type: ignore
    filename = f"{uuid.uuid4()}.{file_ext}"
    input_path = os.path.join(UPLOADS_DIR, filename)

    # Saving the original
    with open(input_path, "wb") as buffer:
        buffer.write(await image.read())

    processed_filename = f"processed_{filename}"
    output_path = os.path.join(BASE_DIR / PROCESSED_DIR, processed_filename)

    # Image classification process
    image_classifier.classification_process(input_path, output_path)
    processed_url = f"processed/{processed_filename}"

    # Returning the processed image
    return templates.TemplateResponse(
        "index.html", {"request": request, "processed_image": processed_url}
    )

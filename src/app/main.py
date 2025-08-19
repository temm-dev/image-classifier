import datetime
import uuid

from config import *
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services import *

app = FastAPI()


templates = Jinja2Templates(directory=BASE_DIR / TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=BASE_DIR / STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=BASE_DIR / UPLOADS_DIR), name="uploads")
app.mount(
    "/processed", StaticFiles(directory=BASE_DIR / PROCESSED_DIR), name="processed"
)


async def process_uploaded_image(image: UploadFile, type_action) -> list:
    """Processes the uploaded image and returns the URL of the processed file"""

    file_ext = image.filename.split(".")[-1]  # type: ignore
    filename = f"{uuid.uuid4()}.{file_ext}"
    image_path = os.path.join(BASE_DIR / UPLOADS_DIR, filename)

    # Saving the original image
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())

    # Image Processing
    processed_filename = f"processed_{filename}"
    output_path = os.path.join(BASE_DIR / PROCESSED_DIR, processed_filename)

    if type_action == "objects":
        list_found = ObjectsClassifier().detect_objects(image_path, output_path)
    elif type_action == "poses":
        list_found = PoseClassifier().detect_poses(image_path, output_path)

    return [f"/processed/{processed_filename}", list_found]




@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Returning the start page"""
    return templates.TemplateResponse(
        "objects.html", {"request": request, "current_time": datetime.datetime.now()}
    )



#|############################################################
#|#                         OBJECTS                          #
#|############################################################

@app.get("/objects", response_class=HTMLResponse)
async def objects_page(request: Request):
    """Returning the start page"""
    return templates.TemplateResponse(
        "objects.html", {"request": request, "current_time": datetime.datetime.now()}
    )

@app.post("/objects/upload")
async def objects_upload_image(request: Request, image: UploadFile = File(...)):
    """Processing of the uploaded image (HTML response)"""
    processed_url, list_found = await process_uploaded_image(image, "objects")
    print(processed_url)

    return templates.TemplateResponse(
        "processed_image.html",
        {"request": request, "processed_image": processed_url},
    )


@app.post("/api/objects/upload")
async def api_objects_upload_image(request: Request, image: UploadFile = File(...)):
    """Processing of the uploaded image (endpoint API)"""
    processed_url, list_found = await process_uploaded_image(image, "objects")

    return {
        "status": "success",
        "processed_image": processed_url,
        "count_found_objects": len(list_found),
        "predictions": list_found
    }



#|############################################################
#|#                          POSES                           #
#|############################################################

@app.get("/poses", response_class=HTMLResponse)
async def poses_page(request: Request):
    """Returning the start page"""
    return templates.TemplateResponse(
        "poses.html", {"request": request, "current_time": datetime.datetime.now()}
    )

@app.post("/poses/upload")
async def poses_upload_image(request: Request, image: UploadFile = File(...)):
    """Processing of the uploaded image (HTML response)"""
    processed_url = await process_uploaded_image(image, "poses")
    return templates.TemplateResponse(
        "processed_image.html",
        {"request": request, "processed_image": processed_url[0]},
    )

@app.post("/api/poses/upload")
async def api_poses_upload_image(request: Request, image: UploadFile = File(...)):
    """Processing of the uploaded image (endpoint API)"""
    processed_url, list_found = await process_uploaded_image(image, "poses")

    return {
        "status": "success",
        "processed_image": processed_url,
        "count_found_poses": len(list_found),
        "predictions": list_found
    }

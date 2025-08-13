import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
UPLOADS_DIR = "uploads"
PROCESSED_DIR = "processed"

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

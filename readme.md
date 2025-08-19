<h1 align="center">🌌 Image Classifier & Object Detector</h1>

<p align="center">
  <img src="assets/capture.png" alt="Project Demo" width="800">
</p>


<div align="center">

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)

</div>


The first project in the study of machine learning: classification of objects in images with definition of boundaries.

## 💡 Project idea
The user uploads a photo → The system:
1. Identifies objects (dog/cat/car/...)
2. Draws a bounding box around each object
3. Returns JSON with coordinates of recognized objects

## ⚙️ Technology stack
### **Backend**
- Python 3.12
- PyTorch
- FastAPI (REST API)
- Uvicorn (ASGI-server)

### **Frontend**
- HTML5 + CSS + JavaScript (simple loading interface)

### **Infrastructure**
- Docker (containerization)

## 🚀 Quick start

### 💻 Local installation
```bash
# Clone a repository
git clone https://github.com/temm-dev/image-classifier.git
cd image-classifier

# Install dependencies
poetry install
# OR
pip install -r requirements.txt

# Launch the app
cd src/app
uvicorn main:app --reload --port 8000
```

### 🐳 Via Docker
#### Use a ready-made image
```bash
docker pull temmdev/image-classifier
docker run --name image-classifier -p 8000:8000 -d temmdev/image-classifier
```


#### Assemble the image yourself
```bash
docker build -t my-image-classifier .
docker run --name my-classifier -p 8000:8000 -d my-image-classifier
```

## 🌐 API Usage

<details><summary style="font-size: 16px; font-weight: bold;">Detect objects</summary>

### Request example via `curl`
```bash
curl -X 'POST' \
  'http://localhost:8000/api/objects/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@path/to/your/image.jpg;type=image/jpeg'
```

### Example of a successful response
```json
{
  "status": "success",
  "processed_image": "processed/processed_image.jpeg",
  "count_found_objects": 3,
  "predictions": [
    {
      "class": "bottle",
      "confidence": 0.9878395199775696,
      "box": [
        261.2372131347656,
        621.8948364257812,
        285.1950378417969,
        690.6560668945312
      ]
    },
    {
      "class": "chair",
      "confidence": 0.9857845902442932,
      "box": [
        653.7933959960938,
        753.1644897460938,
        951.2028198242188,
        1148.4215087890625
      ]
    },
    {
      "class": "person",
      "confidence": 0.9853758215904236,
      "box": [
        604.1263427734375,
        527.564208984375,
        874.9927978515625,
        966.6196899414062
      ]
    }

  ]
}
```
</details>

<details><summary style="font-size: 16px; font-weight: bold;">Detect poses</summary>

### Request example via `curl`
```bash
curl -X 'POST' \
  'http://localhost:8000/api/poses/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@path/to/your/image.jpg;type=image/jpeg'
```

### Example of a successful response
```json
{
  "status": "success",
  "processed_image": "processed/processed_image.jpeg",
  "count_found_poses": 3,
  "predictions": [
    {
      "class": "nose",
      "confidence": 0.9978139400482178,
      "position": [
        815.9758911132812,
        215.8396759033203
      ]
    },
    {
      "class": "left_eye",
      "confidence": 0.9978139400482178,
      "position": [
        835.1710815429688,
        179.88650512695312
      ]
    },
    {
      "class": "right_eye",
      "confidence": 0.9978139400482178,
      "position": [
        782.3843994140625,
        203.85528564453125
      ]
    }
  ]
}
```
</details>

<br>
<br>
<br>

> **Have a nice day!** 🍀
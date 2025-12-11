<h1 align="center">🌌 Image Classifier & Object Detector</h1>

<div align="center">

**A machine learning project for detecting and classifying objects in images with bounding box visualization.**  
*The first step into the world of computer vision.*

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

<p align="center">
  <img src="assets/capture.png" alt="Project Demo" width="700">
</p>

## ✨ Features

* **Object Detection & Classification**: Identifies objects (dog, cat, car, etc.) and draws precise bounding boxes.
* **Pose Estimation**: Detects key body points (nose, eyes, etc.).
* **REST API**: Clean and documented API built with FastAPI.
* **Docker Support**: Ready for containerized deployment.
* **Simple Web Interface**: Easy-to-use frontend for testing.

## 🚀 Quick Start

### Dependencies
* Python 3.12+
* Poetry (recommended) or pip
* Docker (optional)

### Installation & Running

#### Method 1: Local Installation (with Poetry)

```bash
# 1. Clone the repository
git clone https://github.com/temm-dev/image-classifier.git
cd image-classifier

# 2. Install dependencies
poetry install

# 3. Run the application
cd src/app && uvicorn main:app --reload --port 8000
```
#### Method 2: Using Docker

```bash
docker run -p 8000:8000 -d temmdev/image-classifier
```

Or build it yourself:


```bash
docker build -t my-image-classifier .
docker run -p 8000:8000 -d my-image-classifier
```

## 🛠️ Technology Stack
| Component       | Technology |
|----------------|------------|
| **Backend**    | Python 3.12, FastAPI, Uvicorn |
| **ML Framework**| PyTorch, torchvision |
| **Frontend**   | HTML5, CSS3, Vanilla JS |
| **Deployment** | Docker |
| **Package Manager** | Poetry |

## 🤝 Contributing
Contributions are welcome! If you have ideas for improvements or find bugs:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

Please ensure your code follows the existing style and includes relevant tests.

## 📄 License
This project is licensed under the MIT License.
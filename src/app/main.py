from fastapi import FastAPI
from fastapi.responses import HTMLResponse  # Импортируем спец. класс

app = FastAPI()

@app.get("/", response_class=HTMLResponse)  # Указываем тип ответа
async def home_page():
    return 
FROM python:3.12-slim

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /image-classifier
COPY . .

RUN poetry install --no-root

WORKDIR /image-classifier/src/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
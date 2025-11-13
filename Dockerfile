FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config.yml .
RUN mkdir -p /app/data

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py"]
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential nginx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY nginx.conf /etc/nginx/nginx.conf

ENV PYTHONPATH=/app

EXPOSE 10000

CMD uvicorn api.main:api --host 0.0.0.0 --port 8000 & \
    streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 & \
    nginx -g "daemon off;"
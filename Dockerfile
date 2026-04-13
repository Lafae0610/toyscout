FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data output

ENV PORT=5050
EXPOSE ${PORT}

CMD gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --timeout 120

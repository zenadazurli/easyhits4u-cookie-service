FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install browser-use playwright
RUN playwright install chromium
RUN playwright install-deps

WORKDIR /app
COPY app.py .

CMD ["python", "-u", "app.py"]
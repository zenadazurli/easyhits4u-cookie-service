FROM python:3.12-slim

RUN pip install playwright browser-use
RUN playwright install chromium
RUN playwright install-deps

WORKDIR /app
COPY app.py .

CMD ["python", "-u", "app.py"]

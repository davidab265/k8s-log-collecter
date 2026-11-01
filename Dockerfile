FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY k8s_to_loki.py .

CMD ["python", "k8s_to_loki.py"]

FROM python:3.10-slim

WORKDIR /app

COPY k8s_to_loki.py /app/k8s_to_loki.py

RUN pip install kubernetes requests

CMD ["/bin/sh", "-c", "python k8s_to_loki.py"]

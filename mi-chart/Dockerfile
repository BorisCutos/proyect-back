# Imagen compacta compatible con OpenShift (UID aleatorio)
FROM python:3.11-slim

# Paquetes mínimos para psycopg2-binary
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
EXPOSE 3002

# No seteamos USER fijo -> OpenShift asigna un UID aleatorio seguro
CMD ["python", "app.py"]

# 1. Imagen base oficial y ligera de Python
FROM python:3.12-slim

# 2. Evita que Python genere archivos .pyc y fuerza los logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalamos las dependencias primero (para aprovechar la caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el código de la aplicación (ignorando lo que pusimos en .dockerignore)
COPY . .

# 6. Arrancamos Uvicorn escuchando en el puerto dinámico que asigne Render
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
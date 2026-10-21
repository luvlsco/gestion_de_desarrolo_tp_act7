# Imagen base liviana de Python 3.11
FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Primero las dependencias (así Docker las reutiliza si no cambian)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código
COPY . .

# Puerto donde escucha la API (Render inyecta $PORT, en local usa 8000)
EXPOSE 8000

# Arranca el servidor Uvicorn.
# Se usa sh -c para respetar la variable $PORT que asigna Render.
# En local $PORT no existe y usa 8000. No cambia el uso con docker compose.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

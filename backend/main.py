import os
import time
from typing import List

import sentry_sdk
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text

# Sentry: solo se activa si hay DSN (en Render se configura como env var).
# En local sin DSN no hace nada y no rompe nada.
SENTRY_DSN = os.getenv("SENTRY_DSN", "")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,
        environment=os.getenv("ENVIRONMENT", "production"),
    )

# Datos de conexión:
# - En local/docker-compose se arma desde DB_HOST/DB_USER/DB_PASSWORD/DB_NAME.
# - En la nube (Render + Aiven) se usa DATABASE_URL completa que da Aiven.
#   Ejemplo: mysql+pymysql://user:pass@host:port/db
DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_USER = os.getenv("DB_USER", "appuser")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")
    DB_NAME = os.getenv("DB_NAME", "tienda")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

# Aiven exige SSL. Si descargaste el ca.pem, poné SSL_CA=/app/ca.pem
# y subí el archivo junto al backend o como Secret File en Render.
SSL_CA = os.getenv("SSL_CA", "")
connect_args = {"ssl": {"ca": SSL_CA}} if SSL_CA else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)

# Por las dudas, reintenta hasta que la base responda
for intento in range(10):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Conectado a la base de datos")
        break
    except Exception as error:
        print(f"Esperando a la base... intento {intento + 1}: {error}")
        time.sleep(3)

app = FastAPI(title="API TP Docker")

# CORS: permite que un navegador de otro origen consuma la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic define la forma de los datos que devuelve la API
class Usuario(BaseModel):
    id: int
    nombre: str
    email: str

@app.get("/")
def estado():
    return {"mensaje": "API funcionando"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/sentry-debug")
def sentry_debug():
    # Endpoint a propósito para la demo de la Actividad 7:
    # provoca un ZeroDivisionError no controlado para verlo en Sentry.
    division_by_zero = 1 / 0
    return {"nunca": division_by_zero}

@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios():
    with engine.connect() as conn:
        filas = conn.execute(
            text("SELECT id, nombre, email FROM usuarios ORDER BY id")
        ).mappings().all()
    return [dict(fila) for fila in filas]

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int):
    with engine.connect() as conn:
        fila = conn.execute(
            text("SELECT id, nombre, email FROM usuarios WHERE id = :id"),
            {"id": usuario_id},
        ).mappings().first()
    if fila is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return dict(fila)
# test auto jue 22 oct 2026 08:27:00 -03

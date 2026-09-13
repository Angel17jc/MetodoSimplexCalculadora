from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import resolver, sistema
from app.core.config import obtener_configuracion

configuracion = obtener_configuracion()

app = FastAPI(
    title="Simplex Paso a Paso",
    version="0.1.0",
    description="API del método simplex (normal y Dos Fases) que explica cada operación.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=configuracion.cors_origenes,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(sistema.router, prefix="/api/v1")
app.include_router(resolver.router, prefix="/api/v1")

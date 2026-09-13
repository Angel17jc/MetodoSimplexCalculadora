from fastapi import FastAPI

from app.api.v1 import sistema

app = FastAPI(
    title="Simplex Paso a Paso",
    version="0.1.0",
    description="API del método simplex (normal y Dos Fases) que explica cada operación.",
)

app.include_router(sistema.router, prefix="/api/v1")

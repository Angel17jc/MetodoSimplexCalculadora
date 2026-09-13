from collections.abc import Iterator
from functools import lru_cache

from fastapi import HTTPException, status
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.core.config import obtener_configuracion

SIN_BASE_DE_DATOS = (
    "No hay base de datos configurada: define DATABASE_URL para guardar y compartir problemas"
)


@lru_cache
def obtener_motor() -> Engine | None:
    url = obtener_configuracion().database_url
    if url is None:
        return None
    return create_engine(url, pool_pre_ping=True)


def hay_base_de_datos() -> bool:
    return obtener_motor() is not None


def obtener_sesion() -> Iterator[Session]:
    """Dependencia de FastAPI. Responde 503 si la app corre sin base de datos."""
    motor = obtener_motor()
    if motor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=SIN_BASE_DE_DATOS
        )
    with Session(motor) as sesion:
        yield sesion

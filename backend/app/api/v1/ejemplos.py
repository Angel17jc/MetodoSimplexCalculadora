from fastapi import APIRouter

from app.schemas.ejemplo import Ejemplo
from app.services.ejemplos import listar_ejemplos

router = APIRouter(tags=["ejemplos"])


@router.get("/ejemplos", summary="Problemas precargados")
def obtener_ejemplos() -> list[Ejemplo]:
    return list(listar_ejemplos())

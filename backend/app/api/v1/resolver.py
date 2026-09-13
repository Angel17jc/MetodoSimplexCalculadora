from fastapi import APIRouter, HTTPException, status

from app.schemas.problema import Problema
from app.schemas.solucion import RespuestaResolver

router = APIRouter(tags=["simplex"])


@router.post(
    "/resolver",
    summary="Resolver un problema paso a paso",
    description="Devuelve todas las operaciones del desarrollo y el resultado. No guarda nada.",
    responses={status.HTTP_501_NOT_IMPLEMENTED: {"description": "Motor pendiente (Sprint 1)"}},
)
def resolver(problema: Problema) -> RespuestaResolver:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="El motor simplex se implementa en el Sprint 1",
    )

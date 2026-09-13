from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.schemas.guardado import GuardarProblema, ProblemaGuardado

router = APIRouter(prefix="/problemas", tags=["problemas guardados"])

PENDIENTE: dict[int | str, dict[str, Any]] = {
    status.HTTP_501_NOT_IMPLEMENTED: {"description": "Pendiente (Sprint 3)"},
    status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "No hay base de datos configurada"},
}


@router.post(
    "",
    summary="Guardar un problema y obtener su enlace",
    status_code=status.HTTP_201_CREATED,
    responses=PENDIENTE,
)
def guardar_problema(datos: GuardarProblema) -> ProblemaGuardado:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Guardar problemas se implementa en el Sprint 3",
    )


@router.get("/{slug}", summary="Abrir un problema guardado", responses=PENDIENTE)
def obtener_problema(slug: str) -> ProblemaGuardado:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Abrir problemas guardados se implementa en el Sprint 3",
    )

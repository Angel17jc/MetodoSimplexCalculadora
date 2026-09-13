from typing import Any

from fastapi import APIRouter, HTTPException, Response, status

from app.schemas.archivo import ArchivoSimplex
from app.schemas.problema import Problema
from app.schemas.solucion import RespuestaResolver

router = APIRouter(tags=["exportar e importar"])

PENDIENTE: dict[int | str, dict[str, Any]] = {
    status.HTTP_501_NOT_IMPLEMENTED: {"description": "Pendiente (Sprint 3)"}
}


@router.post(
    "/importar",
    summary="Importar un archivo .simplex.json",
    description="Valida el archivo y vuelve a resolver el problema que contiene.",
    responses=PENDIENTE,
)
def importar(archivo: ArchivoSimplex) -> RespuestaResolver:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Importar se implementa en el Sprint 3",
    )


@router.post(
    "/exportar/pdf",
    summary="Exportar el desarrollo completo a PDF",
    response_class=Response,
    responses={
        status.HTTP_200_OK: {"content": {"application/pdf": {}}, "description": "Archivo PDF"},
        **PENDIENTE,
    },
)
def exportar_pdf(problema: Problema) -> Response:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Exportar a PDF se implementa en el Sprint 3",
    )

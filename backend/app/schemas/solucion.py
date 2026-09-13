from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.fraccion import Fraccion
from app.schemas.pasos import Paso
from app.schemas.problema import Problema


class Estado(StrEnum):
    OPTIMO = "optimo"
    MULTIPLES_OPTIMOS = "multiples_optimos"
    NO_ACOTADO = "no_acotado"
    INFACTIBLE = "infactible"


class Clasificacion(BaseModel):
    tipo: Literal["normal", "extendido"]
    motivo: str = Field(examples=["Hay restricciones ≥ y =: se usarán Dos Fases"])


class ResultadoFinal(BaseModel):
    variables: dict[str, Fraccion] = Field(description="Variables de decisión: x1, x2…")
    holguras: dict[str, Fraccion] = Field(description="Holguras y excesos; sin artificiales")
    z: Fraccion


class RespuestaResolver(BaseModel):
    """Desarrollo completo de un problema: todos los pasos y el resultado."""

    version_formato: Literal[1] = 1
    problema: Problema
    clasificacion: Clasificacion
    estado: Estado
    pasos: list[Paso]
    resultado: ResultadoFinal | None = Field(
        default=None, description="Vacío si el problema es infactible o no acotado"
    )

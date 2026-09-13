from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.problema import Problema
from app.schemas.solucion import RespuestaResolver


class ArchivoSimplex(BaseModel):
    """Contenido de un archivo .simplex.json exportado o de un ejemplo precargado.

    Al importar solo se usa `problema`: el backend vuelve a resolver y no confía en `solucion`.
    """

    formato: Literal["simplex-paso-a-paso"] = "simplex-paso-a-paso"
    version_formato: Literal[1] = 1
    titulo: str = Field(default="Problema sin título", min_length=1, max_length=120)
    descripcion: str | None = Field(default=None, max_length=500)
    exportado_en: datetime | None = None
    problema: Problema
    solucion: RespuestaResolver | None = None

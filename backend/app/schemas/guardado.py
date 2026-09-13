from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.problema import Problema
from app.schemas.solucion import RespuestaResolver


class GuardarProblema(BaseModel):
    titulo: str = Field(default="Problema sin título", min_length=1, max_length=120)
    problema: Problema


class ProblemaGuardado(BaseModel):
    slug: str = Field(description="Identificador del enlace para compartir")
    titulo: str
    creado_en: datetime
    problema: Problema
    solucion: RespuestaResolver

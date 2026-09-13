from pydantic import BaseModel, Field

from app.schemas.problema import Problema


class Ejemplo(BaseModel):
    id: str = Field(examples=["profesor-max"])
    titulo: str
    descripcion: str | None = None
    problema: Problema

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.fraccion import Fraccion


class TablaSimplex(BaseModel):
    """Estado de la tabla simplex en un momento del desarrollo."""

    columnas: list[str] = Field(description="Variables en orden: x1, x2, S1, S2, A1…")
    cj: list[Fraccion] = Field(description="Coeficiente de cada columna en el objetivo de la fase")
    base: list[str] = Field(description="Variable básica de cada fila")
    cb: list[Fraccion] = Field(description="Cj de la variable básica de cada fila")
    b: list[Fraccion] = Field(description="Lado derecho de cada fila")
    matriz: list[list[Fraccion]] = Field(description="Coeficientes: una lista por fila")
    nombre_objetivo: Literal["Z", "W"] = Field(description="W en Fase 1, Z en Fase 2")
    fila_z: list[Fraccion] = Field(description="Zj − Cj de cada columna")
    valor_z: Fraccion = Field(description="Valor actual de Z o W")

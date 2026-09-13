from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.fraccion import Fraccion
from app.schemas.tabla import TablaSimplex


class TipoPaso(StrEnum):
    """Cada operación que el modo paso a paso muestra por separado."""

    MODELO_ORIGINAL = "modelo_original"
    CLASIFICACION = "clasificacion"
    FORMA_EXTENDIDA = "forma_extendida"
    TABLA_INICIAL = "tabla_inicial"
    FILA_Z_INICIAL = "fila_z_inicial"
    ANULAR_BASICA_EN_Z = "anular_basica_en_z"
    PRUEBA_OPTIMALIDAD = "prueba_optimalidad"
    VARIABLE_ENTRA = "variable_entra"
    PRUEBA_RAZON = "prueba_razon"
    VARIABLE_SALE = "variable_sale"
    FILA_PIVOTE = "fila_pivote"
    OPERACION_FILA = "operacion_fila"
    FILA_SIN_CAMBIO = "fila_sin_cambio"
    OPERACION_FILA_Z = "operacion_fila_z"
    COMPROBACION_ZJ = "comprobacion_zj"
    SOLUCION_ACTUAL = "solucion_actual"
    FIN_FASE_1 = "fin_fase_1"
    INICIO_FASE_2 = "inicio_fase_2"
    LECTURA_RESULTADO = "lectura_resultado"
    CASO_ESPECIAL = "caso_especial"


class Resaltado(BaseModel):
    """Qué partes de la tabla se destacan en el paso."""

    columnas: list[str] = Field(default_factory=list)
    filas: list[str] = Field(default_factory=list)
    celdas: list[tuple[str, str]] = Field(
        default_factory=list, description="Pares (fila, columna), por ejemplo el pivote"
    )


class RazonFila(BaseModel):
    """Una línea de la prueba de razón mínima."""

    fila: str
    participa: bool
    calculo: str | None = Field(default=None, examples=["500 ÷ 20"])
    resultado: Fraccion | None = None
    motivo: str | None = Field(default=None, examples=["división entre 0: no se considera"])
    menor: bool = False


class OperacionFila(BaseModel):
    """Operación de Gauss-Jordan sobre una fila, valor por valor."""

    fila: str
    latex: str = Field(examples=["R_2' = -20\\,R_3' + R_2"])
    antes: list[Fraccion]
    suma: list[Fraccion] | None = Field(
        default=None, description="Término que se suma, por ejemplo −20·R3'"
    )
    despues: list[Fraccion]


class Paso(BaseModel):
    """Una operación atómica del desarrollo. El puntero del frontend avanza de a uno."""

    indice: int = Field(ge=0)
    fase: Literal[1, 2] | None = None
    iteracion: int | None = Field(default=None, ge=0)
    tipo: TipoPaso
    titulo: str
    texto: str
    latex: str | None = None
    razones: list[RazonFila] | None = None
    operacion: OperacionFila | None = None
    resaltar: Resaltado = Field(default_factory=Resaltado)
    tabla: TablaSimplex | None = Field(
        default=None, description="Cómo queda la tabla después de aplicar el paso"
    )

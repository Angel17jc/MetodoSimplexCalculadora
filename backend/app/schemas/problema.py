from typing import Literal, Self

from pydantic import BaseModel, Field, model_validator

from app.schemas.fraccion import Fraccion

MAX_VARIABLES = 20
MAX_RESTRICCIONES = 50

Objetivo = Literal["max", "min"]
Signo = Literal["<=", ">=", "="]


class Restriccion(BaseModel):
    coeficientes: list[Fraccion] = Field(min_length=1, max_length=MAX_VARIABLES)
    signo: Signo
    lado_derecho: Fraccion


class Problema(BaseModel):
    """Modelo de programación lineal tal como lo escribe el usuario."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "objetivo": "max",
                    "coef_objetivo": ["10", "15"],
                    "restricciones": [
                        {"coeficientes": ["1", ""], "signo": "<=", "lado_derecho": "400"},
                        {"coeficientes": ["15", "20"], "signo": ">=", "lado_derecho": "500"},
                        {"coeficientes": ["", "8"], "signo": "=", "lado_derecho": "100"},
                    ],
                }
            ]
        }
    }

    objetivo: Objetivo
    coef_objetivo: list[Fraccion] = Field(min_length=1, max_length=MAX_VARIABLES)
    restricciones: list[Restriccion] = Field(min_length=1, max_length=MAX_RESTRICCIONES)

    @model_validator(mode="after")
    def validar_cantidad_de_coeficientes(self) -> Self:
        cantidad = len(self.coef_objetivo)
        for numero, restriccion in enumerate(self.restricciones, start=1):
            if len(restriccion.coeficientes) != cantidad:
                raise ValueError(
                    f"La restricción {numero} tiene {len(restriccion.coeficientes)} "
                    f"coeficientes y deben ser {cantidad}, uno por variable"
                )
        return self

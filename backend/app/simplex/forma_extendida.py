"""Forma extendida: cada restricción ≤ recibe su holgura y pasa a ser una igualdad."""

from dataclasses import dataclass
from fractions import Fraction

from app.schemas.problema import Problema
from app.simplex.tabla import Vector, etiqueta_fila


@dataclass(frozen=True)
class FormaExtendida:
    """Sistema a·x + S = b listo para armar la tabla inicial.

    `holguras[i]` es la variable que se sumó en la fila i; su columna es la de la identidad.
    """

    variables: tuple[str, ...]
    holguras: tuple[str, ...]
    matriz: tuple[Vector, ...]
    b: Vector

    @property
    def columnas(self) -> tuple[str, ...]:
        return (*self.variables, *self.holguras)


def construir_forma_extendida(problema: Problema) -> FormaExtendida:
    """Suma una holgura S1, S2… por restricción, en orden: `a·x ≤ b` pasa a `a·x + S = b`."""
    for indice, restriccion in enumerate(problema.restricciones):
        fila = etiqueta_fila(indice)
        if restriccion.signo != "<=":
            raise ValueError(f"{fila} no es ≤: necesita exceso o artificial (Dos Fases)")
        if restriccion.lado_derecho < 0:
            raise ValueError(f"{fila} tiene lado derecho < 0: normaliza el problema primero")

    num_filas = len(problema.restricciones)
    variables = tuple(f"x{numero}" for numero in range(1, len(problema.coef_objetivo) + 1))
    holguras = tuple(f"S{numero}" for numero in range(1, num_filas + 1))
    matriz = tuple(
        (
            *restriccion.coeficientes,
            *(Fraction(1 if columna == indice else 0) for columna in range(num_filas)),
        )
        for indice, restriccion in enumerate(problema.restricciones)
    )
    b = tuple(restriccion.lado_derecho for restriccion in problema.restricciones)
    return FormaExtendida(variables=variables, holguras=holguras, matriz=matriz, b=b)

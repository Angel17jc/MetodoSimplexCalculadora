"""Tabla simplex inmutable: cada operación devuelve una tabla nueva."""

from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Literal, Self

from app.schemas.tabla import TablaSimplex

Vector = tuple[Fraction, ...]
NombreObjetivo = Literal["Z", "W"]


def etiqueta_fila(indice: int) -> str:
    """Nombre de la fila en las operaciones: la primera fila es R1."""
    return f"R{indice + 1}"


@dataclass(frozen=True)
class Tabla:
    """Estado de la tabla en un momento del desarrollo.

    `fila_z` guarda Zj − Cj de cada columna y `valor_z` el valor de su lado derecho.
    """

    columnas: tuple[str, ...]
    cj: Vector
    base: tuple[str, ...]
    cb: Vector
    b: Vector
    matriz: tuple[Vector, ...]
    fila_z: Vector
    valor_z: Fraction
    nombre_objetivo: NombreObjetivo = "Z"

    def __post_init__(self) -> None:
        if len(self.cj) != self.num_columnas or len(self.fila_z) != self.num_columnas:
            raise ValueError("Cj y la fila Z deben tener un valor por columna")
        if not len(self.cb) == len(self.b) == len(self.matriz) == self.num_filas:
            raise ValueError("Cb, b y la matriz deben tener un valor por fila")
        if any(len(fila) != self.num_columnas for fila in self.matriz):
            raise ValueError("Cada fila de la matriz debe tener un valor por columna")

    @property
    def num_filas(self) -> int:
        return len(self.base)

    @property
    def num_columnas(self) -> int:
        return len(self.columnas)

    def columna(self, indice: int) -> Vector:
        return tuple(fila[indice] for fila in self.matriz)

    def fila_completa(self, fila: int) -> Vector:
        """Coeficientes de la fila seguidos de su lado derecho, como se escribe a mano."""
        return (*self.matriz[fila], self.b[fila])

    def fila_z_completa(self) -> Vector:
        return (*self.fila_z, self.valor_z)

    def con_fila(self, fila: int, valores: Vector) -> Self:
        """Copia con la fila reemplazada; `valores` incluye el lado derecho al final."""
        self._validar_largo(valores)
        matriz = tuple(
            valores[:-1] if i == fila else actual for i, actual in enumerate(self.matriz)
        )
        b = tuple(valores[-1] if i == fila else actual for i, actual in enumerate(self.b))
        return replace(self, matriz=matriz, b=b)

    def con_fila_z(self, valores: Vector) -> Self:
        """Copia con la fila Z reemplazada; `valores` incluye el valor de Z al final."""
        self._validar_largo(valores)
        return replace(self, fila_z=valores[:-1], valor_z=valores[-1])

    def con_basica(self, fila: int, columna: int) -> Self:
        """Copia con la variable de la columna como básica de la fila; su Cb pasa a ser su Cj."""
        base = tuple(
            self.columnas[columna] if i == fila else actual for i, actual in enumerate(self.base)
        )
        cb = tuple(self.cj[columna] if i == fila else actual for i, actual in enumerate(self.cb))
        return replace(self, base=base, cb=cb)

    def a_esquema(self) -> TablaSimplex:
        return TablaSimplex(
            columnas=list(self.columnas),
            cj=list(self.cj),
            base=list(self.base),
            cb=list(self.cb),
            b=list(self.b),
            matriz=[list(fila) for fila in self.matriz],
            nombre_objetivo=self.nombre_objetivo,
            fila_z=list(self.fila_z),
            valor_z=self.valor_z,
        )

    def _validar_largo(self, valores: Vector) -> None:
        if len(valores) != self.num_columnas + 1:
            raise ValueError("La fila debe tener un valor por columna más el lado derecho")

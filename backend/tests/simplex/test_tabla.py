from dataclasses import FrozenInstanceError
from fractions import Fraction

import pytest

from app.simplex.tabla import Tabla, etiqueta_fila


def v(*valores: int | str) -> tuple[Fraction, ...]:
    return tuple(Fraction(valor) for valor in valores)


def tabla_ejemplo() -> Tabla:
    return Tabla(
        columnas=("x1", "x2", "S1", "S2"),
        cj=v(3, 5, 0, 0),
        base=("S1", "S2"),
        cb=v(0, 0),
        b=v(4, 12),
        matriz=(v(1, 0, 1, 0), v(0, 2, 0, 1)),
        fila_z=v(3, 5, 0, 0),
        valor_z=Fraction(0),
    )


def test_lee_filas_y_columnas() -> None:
    tabla = tabla_ejemplo()

    assert tabla.num_filas == 2
    assert tabla.num_columnas == 4
    assert tabla.fila_completa(1) == v(0, 2, 0, 1, 12)
    assert tabla.columna(1) == v(0, 2)
    assert tabla.fila_z_completa() == v(3, 5, 0, 0, 0)


def test_rechaza_dimensiones_incorrectas() -> None:
    with pytest.raises(ValueError, match="un valor por columna"):
        Tabla(
            columnas=("x1", "S1"),
            cj=v(1, 0),
            base=("S1",),
            cb=v(0),
            b=v(4),
            matriz=(v(1),),
            fila_z=v(1, 0),
            valor_z=Fraction(0),
        )


def test_con_fila_devuelve_una_copia() -> None:
    original = tabla_ejemplo()

    nueva = original.con_fila(1, v(0, 1, 0, "1/2", 6))

    assert nueva.fila_completa(1) == v(0, 1, 0, "1/2", 6)
    assert original.fila_completa(1) == v(0, 2, 0, 1, 12)
    assert nueva.fila_completa(0) == original.fila_completa(0)


def test_con_fila_z_reemplaza_coeficientes_y_valor() -> None:
    nueva = tabla_ejemplo().con_fila_z(v(-3, 0, 0, "5/2", 30))

    assert nueva.fila_z == v(-3, 0, 0, "5/2")
    assert nueva.valor_z == 30


def test_con_fila_rechaza_largo_incorrecto() -> None:
    with pytest.raises(ValueError, match="lado derecho"):
        tabla_ejemplo().con_fila(0, v(1, 0, 1, 0))


def test_con_basica_cambia_base_y_cb() -> None:
    nueva = tabla_ejemplo().con_basica(1, 1)

    assert nueva.base == ("S1", "x2")
    assert nueva.cb == v(0, 5)


def test_es_inmutable() -> None:
    with pytest.raises(FrozenInstanceError):
        tabla_ejemplo().valor_z = Fraction(1)  # type: ignore[misc]


def test_convierte_al_esquema_con_fracciones_como_texto() -> None:
    esquema = tabla_ejemplo().con_fila(1, v(0, 1, 0, "1/2", 6)).a_esquema()

    datos = esquema.model_dump(mode="json")
    assert datos["b"] == ["4", "6"]
    assert datos["matriz"][1] == ["0", "1", "0", "1/2"]
    assert datos["nombre_objetivo"] == "Z"


def test_etiqueta_de_fila_empieza_en_r1() -> None:
    assert etiqueta_fila(0) == "R1"
    assert etiqueta_fila(2) == "R3"

from fractions import Fraction

import pytest

from app.schemas.problema import Problema, Signo
from app.simplex.forma_extendida import construir_forma_extendida


def v(*valores: int | str) -> tuple[Fraction, ...]:
    return tuple(Fraction(valor) for valor in valores)


def caso_3() -> Problema:
    """Max 3x1 + 5x2; x1 ≤ 4; 2x2 ≤ 12; 3x1 + 2x2 ≤ 18."""
    return Problema.model_validate(
        {
            "objetivo": "max",
            "coef_objetivo": ["3", "5"],
            "restricciones": [
                {"coeficientes": ["1", ""], "signo": "<=", "lado_derecho": "4"},
                {"coeficientes": ["0", "2"], "signo": "<=", "lado_derecho": "12"},
                {"coeficientes": ["3", "2"], "signo": "<=", "lado_derecho": "18"},
            ],
        }
    )


def test_agrega_una_holgura_por_restriccion_en_orden() -> None:
    forma = construir_forma_extendida(caso_3())

    assert forma.variables == ("x1", "x2")
    assert forma.holguras == ("S1", "S2", "S3")
    assert forma.columnas == ("x1", "x2", "S1", "S2", "S3")


def test_las_holguras_forman_la_matriz_identidad() -> None:
    forma = construir_forma_extendida(caso_3())

    assert forma.matriz == (
        v(1, 0, 1, 0, 0),
        v(0, 2, 0, 1, 0),
        v(3, 2, 0, 0, 1),
    )
    assert forma.b == v(4, 12, 18)


def test_acepta_coeficientes_fraccionarios() -> None:
    problema = Problema.model_validate(
        {
            "objetivo": "min",
            "coef_objetivo": ["1"],
            "restricciones": [{"coeficientes": ["3/4"], "signo": "<=", "lado_derecho": "0.5"}],
        }
    )

    forma = construir_forma_extendida(problema)

    assert forma.matriz == (v("3/4", 1),)
    assert forma.b == v("1/2")


@pytest.mark.parametrize("signo", [">=", "="])
def test_rechaza_restricciones_que_necesitan_dos_fases(signo: Signo) -> None:
    problema = caso_3()
    problema.restricciones[1].signo = signo

    with pytest.raises(ValueError, match="R2 no es ≤"):
        construir_forma_extendida(problema)


def test_rechaza_lado_derecho_negativo() -> None:
    problema = caso_3()
    problema.restricciones[2].lado_derecho = Fraction(-18)

    with pytest.raises(ValueError, match="R3 tiene lado derecho < 0"):
        construir_forma_extendida(problema)

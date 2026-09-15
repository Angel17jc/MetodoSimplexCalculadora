from fractions import Fraction

import pytest

from app.schemas.problema import Problema, Signo
from app.simplex.normalizacion import normalizar


def problema(*restricciones: tuple[list[str], Signo, str]) -> Problema:
    return Problema.model_validate(
        {
            "objetivo": "min",
            "coef_objetivo": ["1", "1"],
            "restricciones": [
                {"coeficientes": coeficientes, "signo": signo, "lado_derecho": lado_derecho}
                for coeficientes, signo, lado_derecho in restricciones
            ],
        }
    )


def test_invierte_menor_o_igual_con_lado_derecho_negativo() -> None:
    resultado = normalizar(problema((["-1", "-1"], "<=", "-2")))

    restriccion = resultado.problema.restricciones[0]
    assert restriccion.coeficientes == [Fraction(1), Fraction(1)]
    assert restriccion.signo == ">="
    assert restriccion.lado_derecho == 2
    assert resultado.invertidas == (0,)


@pytest.mark.parametrize(("signo", "esperado"), [(">=", "<="), ("=", "=")])
def test_invierte_el_signo_segun_la_restriccion(signo: Signo, esperado: Signo) -> None:
    resultado = normalizar(problema((["3/2", "-4"], signo, "-5/2")))

    restriccion = resultado.problema.restricciones[0]
    assert restriccion.coeficientes == [Fraction(-3, 2), Fraction(4)]
    assert restriccion.signo == esperado
    assert restriccion.lado_derecho == Fraction(5, 2)


def test_deja_igual_lado_derecho_cero_o_positivo() -> None:
    original = problema((["1", "2"], "<=", "0"), (["-1", "3"], ">=", "4"))

    resultado = normalizar(original)

    assert resultado.problema == original
    assert resultado.invertidas == ()


def test_solo_invierte_las_filas_negativas_y_no_modifica_el_original() -> None:
    original = problema((["1", "0"], "<=", "4"), (["-1", "-1"], "<=", "-2"))

    resultado = normalizar(original)

    assert resultado.invertidas == (1,)
    assert resultado.problema.restricciones[0] == original.restricciones[0]
    assert resultado.problema.restricciones[1].signo == ">="
    assert original.restricciones[1].signo == "<="
    assert original.restricciones[1].lado_derecho == -2

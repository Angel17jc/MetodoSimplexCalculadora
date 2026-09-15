import pytest

from app.schemas.problema import Objetivo, Problema, Signo
from app.simplex.clasificacion import MOTIVO_MAX_NORMAL, MOTIVO_MIN_NORMAL, clasificar


def problema(objetivo: Objetivo, *signos: Signo, lado_derecho: str = "4") -> Problema:
    return Problema.model_validate(
        {
            "objetivo": objetivo,
            "coef_objetivo": ["3", "5"],
            "restricciones": [
                {"coeficientes": ["1", "2"], "signo": signo, "lado_derecho": lado_derecho}
                for signo in signos
            ],
        }
    )


def test_maximizar_con_solo_menor_o_igual_es_normal() -> None:
    clasificacion = clasificar(problema("max", "<=", "<="))

    assert clasificacion.tipo == "normal"
    assert clasificacion.motivo == MOTIVO_MAX_NORMAL


def test_minimizar_con_solo_menor_o_igual_es_normal_sin_fase_1() -> None:
    clasificacion = clasificar(problema("min", "<="))

    assert clasificacion.tipo == "normal"
    assert clasificacion.motivo == MOTIVO_MIN_NORMAL


@pytest.mark.parametrize(
    ("signos", "motivo"),
    [
        ((">=",), "Hay restricciones ≥: se usarán Dos Fases"),
        (("<=", "="), "Hay restricciones =: se usarán Dos Fases"),
        (("<=", ">=", "="), "Hay restricciones ≥ y =: se usarán Dos Fases"),
    ],
)
@pytest.mark.parametrize("objetivo", ["max", "min"])
def test_mayor_o_igual_o_igualdad_es_extendido(
    objetivo: Objetivo, signos: tuple[Signo, ...], motivo: str
) -> None:
    clasificacion = clasificar(problema(objetivo, *signos))

    assert clasificacion.tipo == "extendido"
    assert clasificacion.motivo == motivo


def test_lado_derecho_cero_es_valido() -> None:
    assert clasificar(problema("max", "<=", lado_derecho="0")).tipo == "normal"


def test_rechaza_problema_sin_normalizar() -> None:
    with pytest.raises(ValueError, match="Normaliza"):
        clasificar(problema("max", "<=", lado_derecho="-2"))

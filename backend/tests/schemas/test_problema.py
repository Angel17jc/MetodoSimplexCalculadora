from fractions import Fraction
from typing import Any

import pytest
from pydantic import ValidationError

from app.schemas.problema import MAX_RESTRICCIONES, MAX_VARIABLES, Problema


def problema_del_profesor() -> dict[str, Any]:
    return {
        "objetivo": "max",
        "coef_objetivo": ["10", "15"],
        "restricciones": [
            {"coeficientes": ["1", ""], "signo": "<=", "lado_derecho": "400"},
            {"coeficientes": ["15", "20"], "signo": ">=", "lado_derecho": "500"},
            {"coeficientes": ["", "8"], "signo": "=", "lado_derecho": "100"},
        ],
    }


def test_acepta_el_ejemplo_del_profesor() -> None:
    problema = Problema.model_validate(problema_del_profesor())

    assert problema.objetivo == "max"
    assert problema.restricciones[1].signo == ">="
    assert problema.restricciones[2].lado_derecho == Fraction(100)


def test_coeficientes_en_blanco_valen_cero() -> None:
    problema = Problema.model_validate(problema_del_profesor())

    assert problema.restricciones[0].coeficientes == [Fraction(1), Fraction(0)]
    assert problema.restricciones[2].coeficientes == [Fraction(0), Fraction(8)]


def test_acepta_minimizar() -> None:
    datos = problema_del_profesor() | {"objetivo": "min"}

    assert Problema.model_validate(datos).objetivo == "min"


def test_rechaza_mas_de_20_variables() -> None:
    n = MAX_VARIABLES + 1
    datos = {
        "objetivo": "max",
        "coef_objetivo": ["1"] * n,
        "restricciones": [{"coeficientes": ["1"] * n, "signo": "<=", "lado_derecho": "1"}],
    }

    with pytest.raises(ValidationError):
        Problema.model_validate(datos)


def test_rechaza_mas_de_50_restricciones() -> None:
    datos = {
        "objetivo": "max",
        "coef_objetivo": ["1"],
        "restricciones": [{"coeficientes": ["1"], "signo": "<=", "lado_derecho": "1"}]
        * (MAX_RESTRICCIONES + 1),
    }

    with pytest.raises(ValidationError):
        Problema.model_validate(datos)


def test_rechaza_restriccion_con_cantidad_distinta_de_coeficientes() -> None:
    datos = problema_del_profesor()
    datos["restricciones"][1]["coeficientes"] = ["15"]

    with pytest.raises(ValidationError, match="restricción 2 tiene 1 coeficientes y deben ser 2"):
        Problema.model_validate(datos)


@pytest.mark.parametrize(
    ("campo", "valor"),
    [("objetivo", "maximizar"), ("restricciones", [])],
)
def test_rechaza_campos_invalidos(campo: str, valor: Any) -> None:
    datos = problema_del_profesor() | {campo: valor}

    with pytest.raises(ValidationError):
        Problema.model_validate(datos)


def test_rechaza_signo_invalido() -> None:
    datos = problema_del_profesor()
    datos["restricciones"][0]["signo"] = "<"

    with pytest.raises(ValidationError):
        Problema.model_validate(datos)

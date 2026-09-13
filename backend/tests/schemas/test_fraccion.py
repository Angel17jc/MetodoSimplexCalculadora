from fractions import Fraction
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

from app.schemas.fraccion import Fraccion


class Modelo(BaseModel):
    valor: Fraccion


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("3/4", Fraction(3, 4)),
        ("-2", Fraction(-2)),
        ("0.5", Fraction(1, 2)),
        ("0,5", Fraction(1, 2)),
        (" 12.5 ", Fraction(25, 2)),
        ("", Fraction(0)),
        (None, Fraction(0)),
        (7, Fraction(7)),
        (0.1, Fraction(1, 10)),
    ],
)
def test_convierte_entradas_validas(entrada: Any, esperado: Fraction) -> None:
    assert Modelo(valor=entrada).valor == esperado


@pytest.mark.parametrize("entrada", ["abc", "1/0", "3/", True, [1]])
def test_rechaza_entradas_invalidas(entrada: Any) -> None:
    with pytest.raises(ValidationError, match="fracción"):
        Modelo(valor=entrada)


def test_serializa_como_texto_en_json() -> None:
    assert Modelo(valor="0.5").model_dump(mode="json") == {"valor": "1/2"}


def test_conserva_fraccion_en_python() -> None:
    assert Modelo(valor="0.5").model_dump() == {"valor": Fraction(1, 2)}

from fractions import Fraction

import pytest

from app.simplex.fracciones import a_decimal, a_latex, a_texto


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (Fraction(25, 2), "25/2"),
        (Fraction(-3), "−3"),
        (Fraction(0), "0"),
        (Fraction(-1, 8), "−1/8"),
    ],
)
def test_a_texto(valor: Fraction, esperado: str) -> None:
    assert a_texto(valor) == esperado


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (Fraction(25, 2), r"\frac{25}{2}"),
        (Fraction(-1, 8), r"-\frac{1}{8}"),
        (Fraction(-3), "-3"),
        (Fraction(0), "0"),
    ],
)
def test_a_latex(valor: Fraction, esperado: str) -> None:
    assert a_latex(valor) == esperado


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (Fraction(1, 3), "0.3333"),
        (Fraction(2, 3), "0.6667"),
        (Fraction(25, 2), "12.5"),
        (Fraction(36), "36"),
        (Fraction(-8375, 2), "−4187.5"),
        (Fraction(-1, 100000), "0"),
    ],
)
def test_a_decimal(valor: Fraction, esperado: str) -> None:
    assert a_decimal(valor) == esperado


def test_a_decimal_redondea_la_mitad_hacia_arriba() -> None:
    assert a_decimal(Fraction(1, 8), decimales=2) == "0.13"

"""Formato de fracciones para mostrar. El cálculo siempre usa Fraction exacta."""

import math
from fractions import Fraction

MENOS = "−"


def a_texto(valor: Fraction) -> str:
    """Fracción para leer en pantalla: 25/2, −3, 0. Usa el signo menos tipográfico (−)."""
    return str(valor).replace("-", MENOS)


def a_latex(valor: Fraction) -> str:
    r"""Fracción en LaTeX: \frac{25}{2}, -\frac{1}{8}, -3."""
    if valor.denominator == 1:
        return str(valor.numerator)
    signo = "-" if valor < 0 else ""
    return f"{signo}\\frac{{{abs(valor.numerator)}}}{{{valor.denominator}}}"


def a_decimal(valor: Fraction, decimales: int = 4) -> str:
    """Vista decimal redondeada (la mitad hacia arriba): 1/3 → 0.3333, 25/2 → 12.5.

    Solo sirve para mostrar; nunca se usa para calcular.
    """
    escala = 10**decimales
    escalado = math.floor(abs(valor) * escala + Fraction(1, 2))
    entero, resto = divmod(escalado, escala)
    texto = str(entero)
    if resto:
        texto += "." + f"{resto:0{decimales}d}".rstrip("0")
    return MENOS + texto if valor < 0 and escalado else texto

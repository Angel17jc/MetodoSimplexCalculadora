from fractions import Fraction
from typing import Annotated, Any

from pydantic import PlainSerializer, PlainValidator, WithJsonSchema

MENSAJE_INVALIDO = "Escribe un número, un decimal (0.5) o una fracción (3/4)"


def convertir_a_fraccion(valor: Any) -> Fraction:
    """Convierte la entrada del usuario en una fracción exacta.

    Acepta enteros, decimales con punto o coma, fracciones como texto y campos vacíos (= 0).
    """
    if valor is None:
        return Fraction(0)
    if isinstance(valor, bool):
        raise ValueError(MENSAJE_INVALIDO)
    if isinstance(valor, Fraction):
        return valor
    if isinstance(valor, int):
        return Fraction(valor)
    if isinstance(valor, float):
        # str() evita arrastrar el error binario: 0.1 -> "0.1" -> 1/10
        return Fraction(str(valor))
    if isinstance(valor, str):
        texto = valor.strip().replace(",", ".")
        if texto == "":
            return Fraction(0)
        try:
            return Fraction(texto)
        except (ValueError, ZeroDivisionError) as error:
            raise ValueError(MENSAJE_INVALIDO) from error
    raise ValueError(MENSAJE_INVALIDO)


def formatear_fraccion(valor: Fraction) -> str:
    return str(valor)


Fraccion = Annotated[
    Fraction,
    PlainValidator(convertir_a_fraccion),
    PlainSerializer(formatear_fraccion, return_type=str, when_used="json"),
    WithJsonSchema(
        {
            "type": "string",
            "description": "Número exacto: entero, decimal o fracción. Vacío equivale a 0.",
            "examples": ["3/4", "-2", "0.5"],
        }
    ),
]

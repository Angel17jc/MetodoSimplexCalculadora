"""Deja todos los lados derechos en cero o positivo antes de clasificar el problema."""

from dataclasses import dataclass

from app.schemas.problema import Problema, Restriccion, Signo

SIGNO_INVERTIDO: dict[Signo, Signo] = {"<=": ">=", ">=": "<=", "=": "="}


@dataclass(frozen=True)
class Normalizacion:
    """Problema con b ≥ 0 en cada restricción.

    `invertidas` guarda los índices de las restricciones que se multiplicaron por −1.
    """

    problema: Problema
    invertidas: tuple[int, ...]


def invertir(restriccion: Restriccion) -> Restriccion:
    """Multiplica la restricción por −1: cambia cada signo y ≤ pasa a ≥ (y al revés)."""
    return Restriccion(
        coeficientes=[-coeficiente for coeficiente in restriccion.coeficientes],
        signo=SIGNO_INVERTIDO[restriccion.signo],
        lado_derecho=-restriccion.lado_derecho,
    )


def normalizar(problema: Problema) -> Normalizacion:
    """Multiplica por −1 cada restricción con lado derecho negativo. No modifica el original."""
    invertidas = tuple(
        indice
        for indice, restriccion in enumerate(problema.restricciones)
        if restriccion.lado_derecho < 0
    )
    restricciones = [
        invertir(restriccion) if indice in invertidas else restriccion
        for indice, restriccion in enumerate(problema.restricciones)
    ]
    return Normalizacion(
        problema=problema.model_copy(update={"restricciones": restricciones}),
        invertidas=invertidas,
    )

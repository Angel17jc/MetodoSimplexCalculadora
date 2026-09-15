"""Decide si el problema se resuelve con simplex normal o con simplex extendido (Dos Fases)."""

from app.schemas.problema import Problema
from app.schemas.solucion import Clasificacion

MOTIVO_MAX_NORMAL = (
    "Todas las restricciones son ≤ y los lados derechos son ≥ 0. "
    "Las holguras forman la base inicial, así que se usa simplex directo."
)
MOTIVO_MIN_NORMAL = (
    "Todas las restricciones son ≤ y los lados derechos son ≥ 0. "
    "Las holguras ya forman la base inicial, así que no se necesitan "
    "variables artificiales ni Fase 1."
)


def clasificar(problema: Problema) -> Clasificacion:
    """Simplex extendido si alguna restricción es ≥ o =, porque necesita variable artificial.

    El problema debe venir normalizado: todos los lados derechos ≥ 0.
    """
    if any(restriccion.lado_derecho < 0 for restriccion in problema.restricciones):
        raise ValueError("Normaliza el problema antes de clasificarlo: hay lados derechos < 0")

    signos = {restriccion.signo for restriccion in problema.restricciones}
    con_artificial = [texto for signo, texto in ((">=", "≥"), ("=", "=")) if signo in signos]
    if con_artificial:
        return Clasificacion(
            tipo="extendido",
            motivo=f"Hay restricciones {' y '.join(con_artificial)}: se usarán Dos Fases",
        )
    motivo = MOTIVO_MAX_NORMAL if problema.objetivo == "max" else MOTIVO_MIN_NORMAL
    return Clasificacion(tipo="normal", motivo=motivo)

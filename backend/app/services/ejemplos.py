from functools import lru_cache
from pathlib import Path

from app.schemas.archivo import ArchivoSimplex
from app.schemas.ejemplo import Ejemplo

CARPETA_EJEMPLOS = Path(__file__).resolve().parent.parent / "ejemplos"
EXTENSION = ".simplex.json"

# Orden en que se muestran; los archivos que no estén aquí van al final.
ORDEN = (
    "profesor-max",
    "profesor-min",
    "simplex-normal",
    "dos-fases-min",
    "infactible",
    "no-acotado",
    "optimos-multiples",
)


def _posicion(identificador: str) -> tuple[int, str]:
    indice = ORDEN.index(identificador) if identificador in ORDEN else len(ORDEN)
    return indice, identificador


@lru_cache
def listar_ejemplos() -> tuple[Ejemplo, ...]:
    ejemplos: list[Ejemplo] = []
    for ruta in CARPETA_EJEMPLOS.glob(f"*{EXTENSION}"):
        archivo = ArchivoSimplex.model_validate_json(ruta.read_text(encoding="utf-8"))
        ejemplos.append(
            Ejemplo(
                id=ruta.name.removesuffix(EXTENSION),
                titulo=archivo.titulo,
                descripcion=archivo.descripcion,
                problema=archivo.problema,
            )
        )
    return tuple(sorted(ejemplos, key=lambda ejemplo: _posicion(ejemplo.id)))

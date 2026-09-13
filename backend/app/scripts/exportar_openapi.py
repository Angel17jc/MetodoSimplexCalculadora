"""Genera backend/openapi.json con el contrato de la API.

Uso:
    python -m app.scripts.exportar_openapi              # escribe el archivo
    python -m app.scripts.exportar_openapi --verificar  # falla si está desactualizado
"""

import argparse
import json
import sys
from pathlib import Path

from app.main import app

RUTA_CONTRATO = Path(__file__).resolve().parents[2] / "openapi.json"


def generar_contrato() -> str:
    return json.dumps(app.openapi(), ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Exporta el contrato OpenAPI de la API.")
    parser.add_argument(
        "--verificar",
        action="store_true",
        help="no escribe; termina con error si openapi.json no coincide con el código",
    )
    argumentos = parser.parse_args()
    contenido = generar_contrato()

    if argumentos.verificar:
        actual = RUTA_CONTRATO.read_text(encoding="utf-8") if RUTA_CONTRATO.exists() else ""
        if actual != contenido:
            print(
                "openapi.json no está actualizado. Ejecuta: python -m app.scripts.exportar_openapi",
                file=sys.stderr,
            )
            return 1
        print("openapi.json está actualizado")
        return 0

    RUTA_CONTRATO.write_text(contenido, encoding="utf-8", newline="\n")
    print(f"Contrato escrito en {RUTA_CONTRATO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    """Configuración leída de variables de entorno o del archivo .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    entorno: str = "desarrollo"
    # Opcional: sin DATABASE_URL la app funciona sin base de datos.
    database_url: str | None = None
    # Lista JSON, por ejemplo: CORS_ORIGENES='["http://localhost:5173"]'
    cors_origenes: list[str] = ["http://localhost:5173"]


@lru_cache
def obtener_configuracion() -> Configuracion:
    return Configuracion()

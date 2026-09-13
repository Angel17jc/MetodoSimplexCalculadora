import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, SmallInteger, String, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# JSONB en PostgreSQL; JSON en otros motores (por ejemplo MySQL o SQLite en pruebas).
Documento = JSON().with_variant(JSONB(), "postgresql")


class Base(DeclarativeBase):
    pass


class ProblemaDB(Base):
    __tablename__ = "problemas"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    titulo: Mapped[str] = mapped_column(String(120))
    objetivo: Mapped[str] = mapped_column(Enum("max", "min", name="objetivo"))
    num_variables: Mapped[int] = mapped_column(SmallInteger)
    coef_objetivo: Mapped[list[str]] = mapped_column(Documento)
    slug_publico: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    restricciones: Mapped[list["RestriccionDB"]] = relationship(
        back_populates="problema", cascade="all, delete-orphan", order_by="RestriccionDB.orden"
    )
    soluciones: Mapped[list["SolucionDB"]] = relationship(
        back_populates="problema", cascade="all, delete-orphan"
    )


class RestriccionDB(Base):
    __tablename__ = "restricciones"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    problema_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("problemas.id", ondelete="CASCADE"), index=True
    )
    orden: Mapped[int] = mapped_column(SmallInteger)
    coeficientes: Mapped[list[str]] = mapped_column(Documento)
    signo: Mapped[str] = mapped_column(Enum("<=", ">=", "=", name="signo"))
    lado_derecho: Mapped[str] = mapped_column(String(64))

    problema: Mapped[ProblemaDB] = relationship(back_populates="restricciones")


class SolucionDB(Base):
    __tablename__ = "soluciones"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    problema_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("problemas.id", ondelete="CASCADE"), index=True
    )
    estado: Mapped[str] = mapped_column(
        Enum("optimo", "multiples_optimos", "no_acotado", "infactible", name="estado_solucion")
    )
    clasificacion: Mapped[str] = mapped_column(Enum("normal", "extendido", name="clasificacion"))
    valor_optimo: Mapped[str | None] = mapped_column(String(128))
    num_pasos: Mapped[int] = mapped_column(Integer)
    resultado: Mapped[dict[str, Any]] = mapped_column(Documento)
    version_motor: Mapped[str] = mapped_column(String(20))
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    problema: Mapped[ProblemaDB] = relationship(back_populates="soluciones")

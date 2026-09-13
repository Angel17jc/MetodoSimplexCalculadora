"""crear tablas iniciales

Revision ID: 508b32e816ee
Revises:
Create Date: 2026-09-13 00:19:40.995940

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "508b32e816ee"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

Documento = sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql")

OBJETIVO = sa.Enum("max", "min", name="objetivo")
SIGNO = sa.Enum("<=", ">=", "=", name="signo")
ESTADO_SOLUCION = sa.Enum(
    "optimo", "multiples_optimos", "no_acotado", "infactible", name="estado_solucion"
)
CLASIFICACION = sa.Enum("normal", "extendido", name="clasificacion")


def upgrade() -> None:
    op.create_table(
        "problemas",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("titulo", sa.String(length=120), nullable=False),
        sa.Column("objetivo", OBJETIVO, nullable=False),
        sa.Column("num_variables", sa.SmallInteger(), nullable=False),
        sa.Column("coef_objetivo", Documento, nullable=False),
        sa.Column("slug_publico", sa.String(length=32), nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_problemas_slug_publico"), "problemas", ["slug_publico"], unique=True)

    op.create_table(
        "restricciones",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("problema_id", sa.Uuid(), nullable=False),
        sa.Column("orden", sa.SmallInteger(), nullable=False),
        sa.Column("coeficientes", Documento, nullable=False),
        sa.Column("signo", SIGNO, nullable=False),
        sa.Column("lado_derecho", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["problema_id"], ["problemas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_restricciones_problema_id"), "restricciones", ["problema_id"], unique=False
    )

    op.create_table(
        "soluciones",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("problema_id", sa.Uuid(), nullable=False),
        sa.Column("estado", ESTADO_SOLUCION, nullable=False),
        sa.Column("clasificacion", CLASIFICACION, nullable=False),
        sa.Column("valor_optimo", sa.String(length=128), nullable=True),
        sa.Column("num_pasos", sa.Integer(), nullable=False),
        sa.Column("resultado", Documento, nullable=False),
        sa.Column("version_motor", sa.String(length=20), nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["problema_id"], ["problemas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_soluciones_problema_id"), "soluciones", ["problema_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_soluciones_problema_id"), table_name="soluciones")
    op.drop_table("soluciones")
    op.drop_index(op.f("ix_restricciones_problema_id"), table_name="restricciones")
    op.drop_table("restricciones")
    op.drop_index(op.f("ix_problemas_slug_publico"), table_name="problemas")
    op.drop_table("problemas")

    # PostgreSQL no borra los tipos enum al borrar las tablas.
    enlace = op.get_bind()
    for tipo in (CLASIFICACION, ESTADO_SOLUCION, SIGNO, OBJETIVO):
        tipo.drop(enlace, checkfirst=True)

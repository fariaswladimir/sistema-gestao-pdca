from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, DateTime, Enum, MetaData, Numeric, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid6 import uuid7

CONVENCAO_NOMES = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=CONVENCAO_NOMES)
    type_annotation_map = {
        Decimal: Numeric(18, 4),
        dict[str, Any]: JSON().with_variant(JSONB(), "postgresql"),
        datetime: DateTime(timezone=True),
    }


class ComId:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


def enum(tipo: type[StrEnum]) -> Enum:
    """Enum gravado como texto com CHECK (sem tipo nativo do Postgres: migrações mais simples)."""
    return Enum(
        tipo,
        name=tipo.__name__.lower(),
        native_enum=False,
        create_constraint=True,
        length=30,
        values_callable=lambda e: [m.value for m in e],
    )

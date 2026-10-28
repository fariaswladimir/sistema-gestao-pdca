from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, true
from sqlalchemy.orm import Mapped, mapped_column

from app.dominio.tipos import (
    Consolidacao,
    Farol,
    Natureza,
    Nivel,
    Origem,
    Periodicidade,
    Polaridade,
    StatusCiclo,
)
from app.modelos.base import Base, ComId, enum


class Ciclo(ComId, Base):
    __tablename__ = "ciclo"

    nome: Mapped[str] = mapped_column(unique=True)
    inicio: Mapped[date]
    fim: Mapped[date]
    status: Mapped[StatusCiclo] = mapped_column(enum(StatusCiclo))


class TipoIndicador(ComId, Base):
    __tablename__ = "tipo_indicador"

    nome: Mapped[str] = mapped_column(unique=True)
    nivel: Mapped[Nivel] = mapped_column(enum(Nivel))
    natureza: Mapped[Natureza] = mapped_column(enum(Natureza))
    polaridade: Mapped[Polaridade] = mapped_column(enum(Polaridade))
    consolidacao: Mapped[Consolidacao] = mapped_column(enum(Consolidacao))
    origem: Mapped[Origem] = mapped_column(enum(Origem))


class Indicador(ComId, Base):
    __tablename__ = "indicador"

    codigo: Mapped[str] = mapped_column(unique=True)
    nome: Mapped[str]
    tipo_id: Mapped[UUID] = mapped_column(ForeignKey("tipo_indicador.id", ondelete="RESTRICT"))
    setor_id: Mapped[UUID] = mapped_column(ForeignKey("setor.id", ondelete="RESTRICT"))
    responsavel_id: Mapped[UUID] = mapped_column(ForeignKey("colaborador.id", ondelete="RESTRICT"))
    unidade: Mapped[str]
    periodicidade: Mapped[Periodicidade] = mapped_column(enum(Periodicidade))
    tolerancia_pct: Mapped[Decimal] = mapped_column(default=Decimal("5"), server_default="5")
    ativo: Mapped[bool] = mapped_column(default=True, server_default=true())
    # TODO(F01): objetivo_id, formula_descricao, publicado. TODO(F02): pai_id, peso, caminho (ltree).


class Meta(ComId, Base):
    __tablename__ = "meta"
    __table_args__ = (
        UniqueConstraint("indicador_id", "ciclo_id", "periodo", postgresql_nulls_not_distinct=True),
    )

    indicador_id: Mapped[UUID] = mapped_column(ForeignKey("indicador.id", ondelete="CASCADE"))
    ciclo_id: Mapped[UUID] = mapped_column(ForeignKey("ciclo.id", ondelete="RESTRICT"))
    periodo: Mapped[date | None]  # None = meta do ciclo
    valor: Mapped[Decimal | None]
    valor_min: Mapped[Decimal | None]
    valor_max: Mapped[Decimal | None]


class Medicao(ComId, Base):
    __tablename__ = "medicao"
    __table_args__ = (UniqueConstraint("indicador_id", "periodo"),)

    indicador_id: Mapped[UUID] = mapped_column(ForeignKey("indicador.id", ondelete="CASCADE"))
    periodo: Mapped[date]
    valor: Mapped[Decimal]
    origem: Mapped[Origem] = mapped_column(enum(Origem))
    registrado_por: Mapped[UUID] = mapped_column(ForeignKey("colaborador.id", ondelete="RESTRICT"))
    farol: Mapped[Farol] = mapped_column(enum(Farol))
    justificativa_correcao: Mapped[str | None]

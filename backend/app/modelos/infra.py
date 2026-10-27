from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import Index, func
from sqlalchemy.orm import Mapped, mapped_column

from app.dominio.tipos import AtorTipo, Canal, StatusTarefa
from app.modelos.base import Base, ComId, enum


class EventoAuditoria(ComId, Base):
    __tablename__ = "evento_auditoria"
    __table_args__ = (Index("ix_evento_auditoria_entidade", "entidade", "entidade_id"),)

    entidade: Mapped[str]
    entidade_id: Mapped[UUID]
    acao: Mapped[str]
    antes: Mapped[dict[str, Any] | None]
    depois: Mapped[dict[str, Any] | None]
    ator_id: Mapped[UUID | None]  # sem FK: o histórico sobrevive à exclusão do ator
    ator_tipo: Mapped[AtorTipo] = mapped_column(enum(AtorTipo))
    modelo_ia: Mapped[str | None]
    canal: Mapped[Canal] = mapped_column(enum(Canal))
    em: Mapped[datetime] = mapped_column(server_default=func.now())


class FilaTarefa(ComId, Base):
    __tablename__ = "fila_tarefa"
    __table_args__ = (Index("ix_fila_tarefa_pendentes", "status", "executar_em"),)

    tipo: Mapped[str]
    payload: Mapped[dict[str, Any]]
    status: Mapped[StatusTarefa] = mapped_column(
        enum(StatusTarefa), default=StatusTarefa.pendente, server_default=StatusTarefa.pendente.value
    )
    tentativas: Mapped[int] = mapped_column(default=0, server_default="0")
    executar_em: Mapped[datetime] = mapped_column(server_default=func.now())

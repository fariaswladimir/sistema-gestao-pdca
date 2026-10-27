from uuid import UUID

from sqlalchemy import ForeignKey, true
from sqlalchemy.orm import Mapped, mapped_column

from app.dominio.tipos import Perfil, StatusColaborador
from app.modelos.base import Base, ComId, enum


class Setor(ComId, Base):
    __tablename__ = "setor"

    nome: Mapped[str]
    sigla: Mapped[str]
    setor_pai_id: Mapped[UUID | None] = mapped_column(ForeignKey("setor.id", ondelete="RESTRICT"))
    ativo: Mapped[bool] = mapped_column(default=True, server_default=true())
    # TODO(F01): gestor_id, unidade, caminho (ltree)


class Colaborador(ComId, Base):
    __tablename__ = "colaborador"

    nome: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    setor_id: Mapped[UUID] = mapped_column(ForeignKey("setor.id", ondelete="RESTRICT"))
    perfil: Mapped[Perfil] = mapped_column(enum(Perfil))
    status: Mapped[StatusColaborador] = mapped_column(
        enum(StatusColaborador), default=StatusColaborador.ativo, server_default=StatusColaborador.ativo.value
    )
    sub_oidc: Mapped[str | None] = mapped_column(unique=True)
    # TODO(F01): cargo, gestor_id

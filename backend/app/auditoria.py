"""Trilha de auditoria. Grava na mesma transação da escrita auditada (quem chama faz o commit)."""

from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.dominio.tipos import AtorTipo, Canal
from app.modelos import EventoAuditoria
from app.seguranca.autenticacao import Usuario


def registrar_auditoria(
    sessao: AsyncSession,
    *,
    entidade: str,
    entidade_id: UUID,
    acao: str,
    antes: dict[str, Any] | None,
    depois: dict[str, Any] | None,
    ator: Usuario,
    canal: Canal,
    ator_tipo: AtorTipo = AtorTipo.humano,
    modelo_ia: str | None = None,
) -> None:
    sessao.add(
        EventoAuditoria(
            entidade=entidade,
            entidade_id=entidade_id,
            acao=acao,
            antes=antes,
            depois=depois,
            ator_id=ator.id,
            ator_tipo=ator_tipo,
            modelo_ia=modelo_ia,
            canal=canal,
        )
    )

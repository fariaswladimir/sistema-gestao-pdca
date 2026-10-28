"""Modo local (primeiras versões, sem login): lista quem pode ser escolhido na tela de entrada.

Só existe com `auth_modo=local`; no modo oidc a rota nem é registrada.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.banco import sessao_db
from app.dominio.tipos import StatusColaborador
from app.modelos import Colaborador, Setor

router = APIRouter(prefix="/sessao-local", tags=["sessao"])


class UsuarioLocal(BaseModel):
    id: UUID
    nome: str
    setor: str


@router.get("/usuarios", response_model=list[UsuarioLocal])
async def usuarios(sessao: AsyncSession = Depends(sessao_db)) -> list[UsuarioLocal]:
    """Colaboradores ativos, sem e-mail nem perfil (só o necessário para escolher)."""
    linhas = await sessao.execute(
        select(Colaborador.id, Colaborador.nome, Setor.nome)
        .join(Setor, Colaborador.setor_id == Setor.id)
        .where(Colaborador.status == StatusColaborador.ativo)
        .order_by(Colaborador.nome)
    )
    return [UsuarioLocal(id=i, nome=n, setor=s) for i, n, s in linhas.all()]

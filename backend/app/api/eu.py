from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dominio.tipos import Perfil
from app.seguranca.autenticacao import Usuario, usuario_atual

router = APIRouter(tags=["sessao"])


class EuSaida(BaseModel):
    id: UUID
    nome: str
    perfil: Perfil
    setor_id: UUID


@router.get("/eu", response_model=EuSaida)
async def eu(usuario: Usuario = Depends(usuario_atual)) -> EuSaida:
    return EuSaida(id=usuario.id, nome=usuario.nome, perfil=usuario.perfil, setor_id=usuario.setor_id)

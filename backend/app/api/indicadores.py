from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.banco import sessao_db
from app.esquemas.indicadores import IndicadorDetalhe, IndicadorResumo
from app.relogio import Relogio, obter_relogio
from app.seguranca.autenticacao import Usuario
from app.seguranca.permissoes import exigir_permissao
from app.servicos.indicadores import ServicoIndicadores

router = APIRouter(prefix="/indicadores", tags=["indicadores"])


@router.get("/meus", response_model=list[IndicadorResumo])
async def listar_meus(
    request: Request,
    usuario: Usuario = Depends(exigir_permissao("indicador:ler")),
    sessao: AsyncSession = Depends(sessao_db),
    relogio: Relogio = Depends(obter_relogio),
) -> list[IndicadorResumo]:
    return await ServicoIndicadores(sessao, usuario, relogio, request.app.state.config).listar_meus()


@router.get("/{indicador_id}", response_model=IndicadorDetalhe, responses={404: {"description": "Não encontrado"}})
async def detalhar(
    indicador_id: UUID,
    request: Request,
    usuario: Usuario = Depends(exigir_permissao("indicador:ler")),
    sessao: AsyncSession = Depends(sessao_db),
    relogio: Relogio = Depends(obter_relogio),
) -> IndicadorDetalhe:
    return await ServicoIndicadores(sessao, usuario, relogio, request.app.state.config).detalhar(indicador_id)

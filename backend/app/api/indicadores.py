from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.erros import CORPO_MALFORMADO, NAO_ENCONTRADO, RESPOSTAS_AUTENTICADAS, ErroSaida
from app.banco import sessao_db
from app.esquemas.indicadores import IndicadorDetalhe, IndicadorResumo, MedicaoEntrada, MedicaoSaida
from app.relogio import Relogio, obter_relogio
from app.seguranca.autenticacao import Usuario
from app.seguranca.permissoes import exigir_permissao
from app.servicos.indicadores import ServicoIndicadores
from app.servicos.medicoes import ServicoMedicoes

Periodo = Annotated[
    str, Path(pattern=r"^[1-9]\d{3}-(0[1-9]|1[0-2])$", description="AAAA-MM", examples=["2026-10"])
]

router = APIRouter(prefix="/indicadores", tags=["indicadores"], responses=RESPOSTAS_AUTENTICADAS)


@router.get("/meus", response_model=list[IndicadorResumo])
async def listar_meus(
    request: Request,
    usuario: Usuario = Depends(exigir_permissao("indicador:ler")),
    sessao: AsyncSession = Depends(sessao_db),
    relogio: Relogio = Depends(obter_relogio),
) -> list[IndicadorResumo]:
    return await ServicoIndicadores(sessao, usuario, relogio, request.app.state.config).listar_meus()


@router.get("/{indicador_id}", response_model=IndicadorDetalhe, responses=NAO_ENCONTRADO)
async def detalhar(
    indicador_id: UUID,
    request: Request,
    usuario: Usuario = Depends(exigir_permissao("indicador:ler")),
    sessao: AsyncSession = Depends(sessao_db),
    relogio: Relogio = Depends(obter_relogio),
) -> IndicadorDetalhe:
    return await ServicoIndicadores(sessao, usuario, relogio, request.app.state.config).detalhar(indicador_id)


@router.put(
    "/{indicador_id}/medicoes/{periodo}",
    response_model=MedicaoSaida,
    responses={
        201: {"model": MedicaoSaida, "description": "Medição criada"},
        **CORPO_MALFORMADO,
        **NAO_ENCONTRADO,
        409: {"model": ErroSaida, "description": "Lançamento simultâneo no mesmo período"},
        422: {"model": ErroSaida, "description": "Entrada inválida ou justificativa ausente"},
    },
)
async def registrar_medicao(
    indicador_id: UUID,
    periodo: Periodo,
    entrada: MedicaoEntrada,
    request: Request,
    response: Response,
    usuario: Usuario = Depends(exigir_permissao("medicao:registrar")),
    sessao: AsyncSession = Depends(sessao_db),
    relogio: Relogio = Depends(obter_relogio),
) -> MedicaoSaida:
    """Lança o valor do período (AAAA-MM). Relançar substitui o valor e exige justificativa."""
    servico = ServicoMedicoes(sessao, usuario, relogio, request.app.state.config)
    medicao, criada = await servico.registrar(indicador_id, periodo, entrada)
    response.status_code = 201 if criada else 200
    return medicao

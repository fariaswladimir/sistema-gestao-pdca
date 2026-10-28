"""Dados fictícios de desenvolvimento e demonstração. Idempotente: rodar de novo não duplica nada.

Os usuários espelham `infra/keycloak/realm-gestao.json` (mesmos e-mails).
"""

import asyncio
from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.banco import criar_engine, criar_fabrica
from app.config import obter_configuracao
from app.dominio.tipos import (
    Consolidacao,
    Natureza,
    Nivel,
    Origem,
    Perfil,
    Periodicidade,
    Polaridade,
    StatusCiclo,
)
from app.modelos import Base, Ciclo, Colaborador, Indicador, Meta, Setor, TipoIndicador

COLABORADORES = [
    ("ana", "Piloto", Perfil.colaborador),
    ("bruno", "Outro", Perfil.colaborador),
    ("carlos", "Piloto", Perfil.gestor),
    ("duda", "Sede", Perfil.diretoria),
    ("eva", "Sede", Perfil.escritorio),
    ("root", "Sede", Perfil.admin),
]


async def _obter_ou_criar[M: Base](
    sessao: AsyncSession, modelo: type[M], chave: dict[str, Any], **campos: Any
) -> M:
    existente = (await sessao.execute(select(modelo).filter_by(**chave))).scalar_one_or_none()
    if existente:
        return existente
    obj = modelo(**chave, **campos)
    sessao.add(obj)
    await sessao.flush()
    return obj


async def semear_sessao(sessao: AsyncSession) -> None:
    sede = await _obter_ou_criar(sessao, Setor, {"nome": "Sede"}, sigla="SED")
    setores = {
        "Sede": sede,
        "Piloto": await _obter_ou_criar(sessao, Setor, {"nome": "Piloto"}, sigla="PIL", setor_pai_id=sede.id),
        "Outro": await _obter_ou_criar(sessao, Setor, {"nome": "Outro"}, sigla="OUT", setor_pai_id=sede.id),
    }
    pessoas = {
        login: await _obter_ou_criar(
            sessao,
            Colaborador,
            {"email": f"{login}@exemplo.org"},
            nome=login.capitalize(),
            setor_id=setores[setor].id,
            perfil=perfil,
        )
        for login, setor, perfil in COLABORADORES
    }
    ciclo = await _obter_ou_criar(
        sessao,
        Ciclo,
        {"nome": "2026"},
        inicio=date(2026, 1, 1),
        fim=date(2026, 12, 31),
        status=StatusCiclo.vigente,
    )
    tipo = await _obter_ou_criar(
        sessao,
        TipoIndicador,
        {"nome": "Setor – maior é melhor"},
        nivel=Nivel.setor,
        natureza=Natureza.controle,
        polaridade=Polaridade.maior_melhor,
        consolidacao=Consolidacao.nenhuma,
        origem=Origem.manual,
    )
    for codigo, nome, setor, responsavel in [
        ("IND-01", "Índice de satisfação do cliente", "Piloto", "ana"),
        ("IND-02", "Entregas no prazo", "Outro", "bruno"),
    ]:
        ind = await _obter_ou_criar(
            sessao,
            Indicador,
            {"codigo": codigo},
            nome=nome,
            tipo_id=tipo.id,
            setor_id=setores[setor].id,
            responsavel_id=pessoas[responsavel].id,
            unidade="%",
            periodicidade=Periodicidade.mensal,
            tolerancia_pct=Decimal("5"),
        )
        await _obter_ou_criar(
            sessao, Meta, {"indicador_id": ind.id, "ciclo_id": ciclo.id, "periodo": None}, valor=Decimal("80")
        )
    # TODO(F01): objetivos, mais tipos e 12 meses de histórico.


async def semear(url: str | None = None) -> None:
    engine = criar_engine(url or obter_configuracao().database_url)
    try:
        async with criar_fabrica(engine)() as sessao, sessao.begin():
            await semear_sessao(sessao)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(semear())
    print("seed aplicado")

"""Matriz executável: cada rota protegida × cada perfil × (recurso próprio, recurso de outro).

As rotas são descobertas pela ação marcada em `exigir_permissao`; o esperado vem de matriz.yaml.
Rota nova sem exemplo em EXEMPLOS_PATH/EXEMPLOS_CORPO faz o teste falhar de propósito.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
import yaml
from apoio_testes import dados
from apoio_testes.tokens import cabecalho
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from sqlalchemy import Engine

from app.dominio.tipos import Perfil
from app.main import criar_app

MATRIZ = yaml.safe_load((Path(__file__).parent / "matriz.yaml").read_text("utf-8"))
EXEMPLOS_PATH: dict[str, str] = {"periodo": "2026-10"}
EXEMPLOS_CORPO: dict[str, dict[str, Any]] = {"MedicaoEntrada": {"valor": 80}}


@dataclass(frozen=True)
class RotaProtegida:
    metodo: str
    caminho: str
    acao: str
    corpo: str | None

    def __str__(self) -> str:
        return f"{self.metodo} {self.caminho}"


def _api_routes(rotas: Any) -> Any:
    """Desce nos routers incluídos (FastAPI ≥ 0.160 os guarda como `_IncludedRouter.original_router`).

    Os routers do projeto declaram o prefixo no próprio APIRouter, então `path` já vem completo.
    """
    for rota in rotas:
        if isinstance(rota, APIRoute):
            yield rota
        elif hasattr(rota, "original_router"):
            yield from _api_routes(rota.original_router.routes)


def _rotas_protegidas() -> list[RotaProtegida]:
    rotas = []
    for rota in _api_routes(criar_app().routes):
        acoes = [d.call.acao for d in rota.dependant.dependencies if hasattr(d.call, "acao")]
        corpo = rota.body_field.field_info.annotation.__name__ if rota.body_field else None
        for metodo in rota.methods:
            rotas.extend(RotaProtegida(metodo, rota.path, acao, corpo) for acao in acoes)
    return sorted(rotas, key=str)


ROTAS = _rotas_protegidas()


def test_ha_rotas_protegidas() -> None:
    assert {r.acao for r in ROTAS} >= {"indicador:ler", "medicao:registrar"}


def _esperado_proprio(acao: str, perfil: Perfil) -> set[int]:
    return {403} if MATRIZ[acao][perfil.value] == "negado" else {200, 201}


@pytest.fixture
def arranjo(engine: Engine, request: pytest.FixtureRequest) -> dict[str, Any]:
    perfil: Perfil = request.node.callspec.params["perfil"]
    with engine.begin() as con:
        a, b = dados.setor(con, "Setor A"), dados.setor(con, "Setor B")
        usuario = dados.colaborador(con, perfil.value, a, perfil=perfil.value)
        alheio = dados.colaborador(con, "alheio", b)
        return {
            "login": perfil.value,
            "proprio": dados.indicador(con, "IND-A", a, usuario),
            "alheio": dados.indicador(con, "IND-B", b, alheio),
        }


def _chamar(cliente: TestClient, rota: RotaProtegida, login: str, indicador_id: Any) -> int:
    params = {**EXEMPLOS_PATH, "indicador_id": str(indicador_id)}
    caminho = rota.caminho.format(**params)
    corpo = EXEMPLOS_CORPO[rota.corpo] if rota.corpo else None
    return cliente.request(rota.metodo, caminho, json=corpo, headers=cabecalho(login)).status_code


@pytest.mark.parametrize("perfil", list(Perfil), ids=lambda p: p.value)
@pytest.mark.parametrize("rota", ROTAS, ids=str)
def test_recurso_proprio(cliente: TestClient, arranjo: dict[str, Any], rota: RotaProtegida, perfil: Perfil) -> None:
    status = _chamar(cliente, rota, arranjo["login"], arranjo["proprio"])
    assert status in _esperado_proprio(rota.acao, perfil), f"{perfil} em {rota}: {status}"


@pytest.mark.parametrize("perfil", list(Perfil), ids=lambda p: p.value)
@pytest.mark.parametrize("rota", [r for r in ROTAS if "{indicador_id}" in r.caminho], ids=str)
def test_recurso_de_outro_responsavel(
    cliente: TestClient, arranjo: dict[str, Any], rota: RotaProtegida, perfil: Perfil
) -> None:
    # Perfil negado: 403 antes de olhar o recurso. Permitido: 404, sem revelar que o recurso existe.
    # TODO(F01): diretoria, escritório e admin passam a ver toda a organização.
    esperado = 403 if MATRIZ[rota.acao][perfil.value] == "negado" else 404
    assert _chamar(cliente, rota, arranjo["login"], arranjo["alheio"]) == esperado

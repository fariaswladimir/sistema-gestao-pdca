"""Fixtures compartilhadas (plugin pytest): API real + Postgres real."""

from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine

from apoio_testes import banco, tokens

# Data congelada dos testes: período atual = 2026-10.
AGORA = datetime(2026, 10, 15, 12, 0, tzinfo=UTC)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def url_banco() -> Iterator[str]:
    with banco.banco_de_testes() as url:
        banco.aplicar_migracoes(url)
        yield url


@pytest.fixture(scope="session")
def engine(url_banco: str) -> Iterator[Engine]:
    eng = create_engine(url_banco)
    yield eng
    eng.dispose()


@pytest.fixture(autouse=True)
def _banco_limpo(request: pytest.FixtureRequest) -> Iterator[None]:
    yield
    if "engine" in request.fixturenames:
        banco.limpar(request.getfixturevalue("engine"))


@pytest.fixture
def cliente(url_banco: str) -> Iterator[TestClient]:
    """API no modo oidc com perfis ativos: o fluxo de login e a matriz que serão religados depois."""
    yield from _cliente(url_banco, auth_modo="oidc", perfis_ativos=True)


@pytest.fixture
def cliente_local(url_banco: str) -> Iterator[TestClient]:
    """API como roda hoje (diretrizes de versão): usuário escolhido, sem perfis."""
    yield from _cliente(url_banco, auth_modo="local", perfis_ativos=False)


def _cliente(url_banco: str, **ajustes: Any) -> Iterator[TestClient]:
    from app.config import Configuracao
    from app.main import criar_app
    from app.relogio import RelogioFixo, obter_relogio
    from app.seguranca.autenticacao import ValidadorToken, obter_validador

    config = Configuracao(
        database_url=banco.url_async(url_banco),
        oidc_issuer=tokens.EMISSOR,
        oidc_audience=tokens.AUDIENCIA,
        app_version="teste",
        **ajustes,
    )
    app = criar_app(config)
    validador = ValidadorToken(
        emissor=tokens.EMISSOR, audiencia=tokens.AUDIENCIA, obter_jwks=lambda forcar=False: tokens.jwks()
    )
    app.dependency_overrides[obter_validador] = lambda: validador
    app.dependency_overrides[obter_relogio] = lambda: RelogioFixo(AGORA)
    with TestClient(app) as c:
        yield c

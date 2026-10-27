"""Fixtures compartilhadas (plugin pytest): API real + Postgres real."""

from collections.abc import Iterator
from datetime import UTC, datetime

import pytest
from apoio_testes import banco, tokens
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine

# Data congelada dos testes: período atual = 2026-10.
AGORA = datetime(2026, 10, 15, 12, 0, tzinfo=UTC)


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
    from app.config import Configuracao
    from app.main import criar_app
    from app.relogio import RelogioFixo, obter_relogio
    from app.seguranca.autenticacao import ValidadorToken, obter_validador

    config = Configuracao(
        database_url=banco.url_async(url_banco),
        oidc_issuer=tokens.EMISSOR,
        oidc_audience=tokens.AUDIENCIA,
        app_version="teste",
    )
    app = criar_app(config)
    validador = ValidadorToken(emissor=tokens.EMISSOR, audiencia=tokens.AUDIENCIA, obter_jwks=tokens.jwks)
    app.dependency_overrides[obter_validador] = lambda: validador
    app.dependency_overrides[obter_relogio] = lambda: RelogioFixo(AGORA)
    with TestClient(app) as c:
        yield c


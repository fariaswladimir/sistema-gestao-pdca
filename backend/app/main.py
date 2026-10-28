from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import eu, indicadores, saude, sessao_local
from app.api.erros import registrar_tratamento_de_erros
from app.banco import criar_engine, criar_fabrica
from app.config import Configuracao, obter_configuracao
from app.logs import configurar_logs, middleware_request_id
from app.seguranca.autenticacao import JwksRemoto, ValidadorToken


def criar_app(config: Configuracao | None = None) -> FastAPI:
    config = config or obter_configuracao()
    configurar_logs(json=config.log_json)

    @asynccontextmanager
    async def ciclo_de_vida(app: FastAPI) -> AsyncGenerator[None]:
        engine = criar_engine(config.database_url)
        app.state.fabrica_sessao = criar_fabrica(engine)
        yield
        await engine.dispose()

    app = FastAPI(title="Sistema de Gestão PDCA e SDCA", version=config.app_version, lifespan=ciclo_de_vida)
    app.state.config = config
    app.state.validador = ValidadorToken(
        emissor=config.oidc_issuer,
        audiencia=config.oidc_audience,
        obter_jwks=JwksRemoto(config.oidc_jwks_url),
    )
    registrar_tratamento_de_erros(app)
    app.middleware("http")(middleware_request_id)
    app.include_router(saude.router)
    app.include_router(eu.router)
    app.include_router(indicadores.router)
    if config.auth_modo == "local":
        app.include_router(sessao_local.router)
    return app


app = criar_app()

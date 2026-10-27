from fastapi import FastAPI

from app.config import Configuracao, obter_configuracao


def criar_app(config: Configuracao | None = None) -> FastAPI:
    config = config or obter_configuracao()
    app = FastAPI(title="Sistema de Gestão PDCA e SDCA", version=config.app_version)
    app.state.config = config
    return app


app = criar_app()

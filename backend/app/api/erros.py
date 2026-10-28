from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.dominio.erros import ErroDominio, NaoAutenticado


async def _tratar(request: Request, erro: Exception) -> JSONResponse:
    assert isinstance(erro, ErroDominio)
    cabecalhos = {"WWW-Authenticate": "Bearer"} if isinstance(erro, NaoAutenticado) else None
    return JSONResponse(status_code=erro.status_http, content={"detalhe": erro.mensagem}, headers=cabecalhos)


def registrar_tratamento_de_erros(app: FastAPI) -> None:
    app.add_exception_handler(ErroDominio, _tratar)

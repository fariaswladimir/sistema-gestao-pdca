"""Envelope único de erro `{detalhe, erros?}` (domínio, validação e framework), documentado no OpenAPI."""

from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from app.dominio.erros import ErroDominio, NaoAutenticado


class ErroSaida(BaseModel):
    detalhe: str
    erros: list[dict[str, Any]] | None = None


def _resposta(descricao: str) -> dict[str, Any]:
    return {"model": ErroSaida, "description": descricao}


RESPOSTAS_AUTENTICADAS: dict[int | str, dict[str, Any]] = {
    401: _resposta("Sem token ou token inválido"),
    403: _resposta("Perfil sem permissão ou usuário sem cadastro ativo"),
    422: _resposta("Entrada inválida"),
}
NAO_ENCONTRADO: dict[int | str, dict[str, Any]] = {404: _resposta("Não encontrado (ou fora do seu escopo)")}
CORPO_MALFORMADO: dict[int | str, dict[str, Any]] = {400: _resposta("Corpo da requisição não é JSON válido")}


async def _tratar_dominio(request: Request, erro: Exception) -> JSONResponse:
    assert isinstance(erro, ErroDominio)
    cabecalhos = {"WWW-Authenticate": "Bearer"} if isinstance(erro, NaoAutenticado) else None
    corpo = ErroSaida(detalhe=erro.mensagem).model_dump(exclude_none=True)
    return JSONResponse(status_code=erro.status_http, content=corpo, headers=cabecalhos)


async def _tratar_validacao(request: Request, erro: Exception) -> JSONResponse:
    assert isinstance(erro, RequestValidationError)
    erros = [{"campo": ".".join(map(str, e["loc"])), "mensagem": e["msg"]} for e in erro.errors()]
    corpo = ErroSaida(detalhe="Entrada inválida.", erros=jsonable_encoder(erros))
    return JSONResponse(status_code=422, content=corpo.model_dump())


async def _tratar_http(request: Request, erro: Exception) -> JSONResponse:
    """Erros do próprio framework (JSON malformado, 404 de rota, 405) no mesmo envelope."""
    assert isinstance(erro, HTTPException)
    corpo = ErroSaida(detalhe=str(erro.detail)).model_dump(exclude_none=True)
    return JSONResponse(status_code=erro.status_code, content=corpo, headers=erro.headers)


def registrar_tratamento_de_erros(app: FastAPI) -> None:
    app.add_exception_handler(ErroDominio, _tratar_dominio)
    app.add_exception_handler(RequestValidationError, _tratar_validacao)
    app.add_exception_handler(HTTPException, _tratar_http)

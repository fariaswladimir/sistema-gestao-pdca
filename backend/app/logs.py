"""Logs estruturados. Nunca registrar e-mail, token ou valor de meta individual."""

import logging
import sys
import uuid
from collections.abc import Awaitable, Callable

import structlog
from fastapi import Request, Response


def configurar_logs(json: bool) -> None:
    processadores: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer() if json else structlog.dev.ConsoleRenderer(),
    ]
    structlog.configure(
        processors=processadores,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.PrintLoggerFactory(sys.stdout),
        cache_logger_on_first_use=True,
    )


async def middleware_request_id(
    request: Request, proximo: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id, metodo=request.method, rota=request.url.path)
    resposta = await proximo(request)
    resposta.headers["x-request-id"] = request_id
    if resposta.status_code >= 500:
        structlog.get_logger().error("requisicao_falhou", status=resposta.status_code)
    return resposta

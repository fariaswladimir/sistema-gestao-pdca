from typing import Literal

import structlog
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.banco import sessao_db

router = APIRouter(tags=["saude"])


class SaudeSaida(BaseModel):
    status: Literal["ok", "degradado"]
    versao: str
    banco: Literal["ok", "falha"]


@router.get("/saude", response_model=SaudeSaida, responses={503: {"model": SaudeSaida}})
async def saude(request: Request, sessao: AsyncSession = Depends(sessao_db)) -> SaudeSaida | JSONResponse:
    versao = request.app.state.config.app_version
    try:
        await sessao.execute(text("select 1"))
    except Exception:
        structlog.get_logger().exception("saude_banco_falhou")
        corpo = SaudeSaida(status="degradado", versao=versao, banco="falha")
        return JSONResponse(status_code=503, content=corpo.model_dump())
    return SaudeSaida(status="ok", versao=versao, banco="ok")

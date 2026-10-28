"""Autenticação: resolve o colaborador da requisição.

Modo `oidc`: valida o access token do Keycloak. Modo `local` (primeiras versões, sem login): confia no
colaborador escolhido na tela de entrada, enviado pela web no cabeçalho `X-Usuario-Local`.
Perfil e setor vêm do banco, nunca de papéis do Keycloak.
"""

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from uuid import UUID

import anyio
import httpx
import jwt
import structlog
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.banco import sessao_db
from app.dominio.erros import NaoAutenticado, SemPermissao
from app.dominio.tipos import Perfil, StatusColaborador
from app.modelos import Colaborador

ObterJwks = Callable[[bool], dict[str, Any]]


@dataclass(frozen=True)
class Usuario:
    id: UUID
    nome: str
    perfil: Perfil
    setor_id: UUID


class JwksRemoto:
    """Busca o JWKS do Keycloak com cache; `forcar=True` renova (rotação de chave)."""

    def __init__(self, url: str, validade_s: int = 3600) -> None:
        self._url = url
        self._validade_s = validade_s
        self._cache: dict[str, Any] | None = None
        self._buscado_em = 0.0

    def __call__(self, forcar: bool = False) -> dict[str, Any]:
        if forcar or self._cache is None or time.monotonic() - self._buscado_em > self._validade_s:
            resposta = httpx.get(self._url, timeout=5)
            resposta.raise_for_status()
            self._cache = resposta.json()
            self._buscado_em = time.monotonic()
        return self._cache


class ValidadorToken:
    def __init__(self, emissor: str, audiencia: str, obter_jwks: ObterJwks) -> None:
        self.emissor = emissor
        self.audiencia = audiencia
        self._obter_jwks = obter_jwks

    async def validar(self, token: str) -> dict[str, Any]:
        try:
            kid = jwt.get_unverified_header(token).get("kid")
            chave = await self._chave(kid)
            claims: dict[str, Any] = jwt.decode(
                token,
                key=chave,
                algorithms=["RS256"],
                audience=self.audiencia,
                issuer=self.emissor,
                options={"require": ["exp", "iss", "aud", "sub"]},
            )
        except jwt.PyJWTError as erro:
            structlog.get_logger().info("token_recusado", motivo=type(erro).__name__)
            raise NaoAutenticado("Token inválido.") from erro
        return claims

    async def _chave(self, kid: str | None) -> Any:
        for forcar in (False, True):
            jwks = await anyio.to_thread.run_sync(self._obter_jwks, forcar)
            for jwk in jwks.get("keys", []):
                if jwk.get("kid") == kid:
                    return jwt.PyJWK(jwk).key
        raise jwt.InvalidKeyError("kid desconhecido")


def obter_validador(request: Request) -> ValidadorToken:
    validador: ValidadorToken = request.app.state.validador
    return validador


_bearer = HTTPBearer(auto_error=False)


CABECALHO_LOCAL = "X-Usuario-Local"


async def usuario_atual(
    request: Request,
    credenciais: HTTPAuthorizationCredentials | None = Depends(_bearer),
    validador: ValidadorToken = Depends(obter_validador),
    sessao: AsyncSession = Depends(sessao_db),
) -> Usuario:
    colaborador: Colaborador | None
    if request.app.state.config.auth_modo == "local":
        colaborador = await _escolhido_localmente(sessao, request.headers.get(CABECALHO_LOCAL))
    else:
        if credenciais is None:
            raise NaoAutenticado("Autenticação necessária.")
        claims = await validador.validar(credenciais.credentials)
        colaborador = await _vincular(sessao, claims)
    if colaborador is None or colaborador.status != StatusColaborador.ativo:
        raise SemPermissao("Usuário sem cadastro ativo no sistema.")
    return Usuario(
        id=colaborador.id, nome=colaborador.nome, perfil=colaborador.perfil, setor_id=colaborador.setor_id
    )


async def _vincular(sessao: AsyncSession, claims: dict[str, Any]) -> Colaborador | None:
    """Acha o colaborador pelo `sub`; no primeiro acesso, pelo e-mail verificado, gravando o `sub`."""
    sub = claims["sub"]
    colaborador = (
        await sessao.execute(select(Colaborador).where(Colaborador.sub_oidc == sub))
    ).scalar_one_or_none()
    if colaborador or not claims.get("email_verified") or not claims.get("email"):
        return colaborador
    colaborador = (
        await sessao.execute(select(Colaborador).where(Colaborador.email == claims["email"].lower()))
    ).scalar_one_or_none()
    if colaborador is None or colaborador.sub_oidc is not None:
        return None
    colaborador.sub_oidc = sub
    await sessao.commit()
    return colaborador


async def _escolhido_localmente(sessao: AsyncSession, valor: str | None) -> Colaborador:
    try:
        colaborador_id = UUID(valor or "")
    except ValueError:
        raise NaoAutenticado("Escolha um usuário para entrar.") from None
    colaborador = await sessao.get(Colaborador, colaborador_id)
    if colaborador is None:
        raise NaoAutenticado("Escolha um usuário para entrar.")
    return colaborador

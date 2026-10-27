"""Emissor de tokens OIDC de teste: chave RSA local no lugar do Keycloak."""

import time
from functools import lru_cache
from typing import Any

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from jwt.algorithms import RSAAlgorithm

EMISSOR = "http://keycloak.teste/realms/gestao"
AUDIENCIA = "gestao-api"
KID = "chave-teste"


@lru_cache
def _chave() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def jwks() -> dict[str, Any]:
    publica: dict[str, Any] = RSAAlgorithm.to_jwk(_chave().public_key(), as_dict=True)
    publica.update(kid=KID, use="sig", alg="RS256")
    return {"keys": [publica]}


def emitir_token(
    sub: str,
    email: str,
    *,
    emissor: str = EMISSOR,
    audiencia: str = AUDIENCIA,
    expira_em_s: int = 300,
    chave: rsa.RSAPrivateKey | None = None,
) -> str:
    agora = int(time.time())
    claims = {
        "iss": emissor,
        "aud": audiencia,
        "sub": sub,
        "email": email,
        "email_verified": True,
        "iat": agora,
        "exp": agora + expira_em_s,
    }
    return jwt.encode(claims, chave or _chave(), algorithm="RS256", headers={"kid": KID})


def cabecalho(login: str) -> dict[str, str]:
    """Cabeçalho Authorization de um usuário de teste. O `sub` é estável por login."""
    return {"Authorization": f"Bearer {emitir_token(sub=f'sub-{login}', email=f'{login}@exemplo.org')}"}

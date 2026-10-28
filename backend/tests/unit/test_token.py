from typing import Any

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from apoio_testes import tokens
from app.dominio.erros import NaoAutenticado
from app.seguranca.autenticacao import ValidadorToken

pytestmark = pytest.mark.anyio


def _validador(obter_jwks: Any = None) -> ValidadorToken:
    return ValidadorToken(
        emissor=tokens.EMISSOR,
        audiencia=tokens.AUDIENCIA,
        obter_jwks=obter_jwks or (lambda forcar=False: tokens.jwks()),
    )


async def test_token_valido_devolve_claims() -> None:
    claims = await _validador().validar(tokens.emitir_token("sub-1", "ana@exemplo.org"))
    assert claims["sub"] == "sub-1"
    assert claims["email"] == "ana@exemplo.org"


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(lambda: tokens.emitir_token("s", "e@x", expira_em_s=-60), id="expirado"),
        pytest.param(
            lambda: tokens.emitir_token("s", "e@x", emissor="http://outro/realms/x"), id="emissor-errado"
        ),
        pytest.param(lambda: tokens.emitir_token("s", "e@x", audiencia="outra-api"), id="audiencia-errada"),
        pytest.param(
            lambda: tokens.emitir_token(
                "s", "e@x", chave=rsa.generate_private_key(public_exponent=65537, key_size=2048)
            ),
            id="assinatura-invalida",
        ),
        pytest.param(lambda: "nao-e-um-jwt", id="malformado"),
    ],
)
async def test_token_invalido_e_recusado(token: Any) -> None:
    with pytest.raises(NaoAutenticado):
        await _validador().validar(token())


async def test_kid_desconhecido_renova_jwks_uma_vez() -> None:
    chamadas: list[bool] = []

    def obter(forcar: bool = False) -> dict[str, Any]:
        chamadas.append(forcar)
        return tokens.jwks() if forcar else {"keys": []}

    await _validador(obter).validar(tokens.emitir_token("s", "e@x"))
    assert chamadas == [False, True]

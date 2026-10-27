"""Validação dos tokens OIDC emitidos pelo Keycloak."""

from collections.abc import Callable
from typing import Any


class ValidadorToken:
    def __init__(self, emissor: str, audiencia: str, obter_jwks: Callable[[], dict[str, Any]]) -> None:
        self.emissor = emissor
        self.audiencia = audiencia
        self._obter_jwks = obter_jwks


def obter_validador() -> ValidadorToken:
    raise NotImplementedError  # T6

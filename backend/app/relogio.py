"""Relógio injetável: o "período atual" depende dele e os testes o congelam."""

from datetime import UTC, datetime
from typing import Protocol


class Relogio(Protocol):
    def agora(self) -> datetime: ...


class RelogioSistema:
    def agora(self) -> datetime:
        return datetime.now(UTC)


class RelogioFixo:
    def __init__(self, instante: datetime) -> None:
        self._instante = instante

    def agora(self) -> datetime:
        return self._instante


def obter_relogio() -> Relogio:
    return RelogioSistema()

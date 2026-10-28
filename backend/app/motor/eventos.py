"""Eventos de domínio. Publicar = gravar em `fila_tarefa` na mesma transação (outbox); o worker consome."""

from dataclasses import asdict, dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modelos import FilaTarefa


@dataclass(frozen=True)
class Evento:
    def payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MedicaoRegistrada(Evento):
    indicador_id: str
    periodo: str
    valor: str
    farol: str
    farol_anterior: str | None


def publicar(sessao: AsyncSession, evento: Evento) -> None:
    sessao.add(FilaTarefa(tipo=type(evento).__name__, payload=evento.payload()))

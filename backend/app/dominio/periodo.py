"""Períodos de medição: `date` no dia 1 do mês; na API, texto `AAAA-MM`."""

import re
from datetime import date, datetime
from zoneinfo import ZoneInfo

from app.dominio.erros import EntradaInvalida

_FORMATO = re.compile(r"^([1-9]\d{3})-(0[1-9]|1[0-2])$")


def de_texto(texto: str) -> date:
    casamento = _FORMATO.match(texto)
    if not casamento:
        raise EntradaInvalida(f"Período inválido: {texto!r}. Use AAAA-MM.")
    return date(int(casamento.group(1)), int(casamento.group(2)), 1)


def para_texto(periodo: date) -> str:
    return periodo.strftime("%Y-%m")


def atual(agora: datetime, fuso: str) -> date:
    local = agora.astimezone(ZoneInfo(fuso))
    return date(local.year, local.month, 1)

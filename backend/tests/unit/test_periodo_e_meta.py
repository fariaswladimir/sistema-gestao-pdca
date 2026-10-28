from datetime import UTC, date, datetime
from decimal import Decimal as D

import pytest

from app.dominio import periodo
from app.dominio.erros import EntradaInvalida
from app.dominio.metas import meta_vigente
from app.motor.farol import MetaValores


def test_periodo_de_texto() -> None:
    assert periodo.de_texto("2026-10") == date(2026, 10, 1)
    assert periodo.para_texto(date(2026, 10, 1)) == "2026-10"


@pytest.mark.parametrize("texto", ["2026-13", "2026-00", "2026-1", "26-10", "2026-10-01", ""])
def test_periodo_invalido(texto: str) -> None:
    with pytest.raises(EntradaInvalida):
        periodo.de_texto(texto)


def test_periodo_atual_usa_fuso_de_recife() -> None:
    # 1º de novembro, 01h UTC = 31 de outubro, 22h em Recife
    assert periodo.atual(datetime(2026, 11, 1, 1, 0, tzinfo=UTC), "America/Recife") == date(2026, 10, 1)


def test_meta_do_periodo_prevalece_sobre_a_do_ciclo() -> None:
    ciclo, outubro = MetaValores(valor=D("80")), MetaValores(valor=D("90"))
    metas = [(None, ciclo), (date(2026, 10, 1), outubro)]
    assert meta_vigente(metas, date(2026, 10, 1)) == outubro
    assert meta_vigente(metas, date(2026, 9, 1)) == ciclo
    assert meta_vigente([], date(2026, 9, 1)) is None

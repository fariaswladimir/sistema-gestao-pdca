from decimal import Decimal as D

import pytest

from app.dominio.tipos import Farol, Polaridade
from app.motor.farol import MetaValores, calcular_farol

MAIOR = Polaridade.maior_melhor
MENOR = Polaridade.menor_melhor
FAIXA = Polaridade.faixa


@pytest.mark.parametrize(
    ("polaridade", "meta", "valor", "tolerancia", "esperado"),
    [
        # maior_melhor (F00 RN4): meta 80, tolerância 5% => amarelo a partir de 76
        (MAIOR, MetaValores(valor=D("80")), D("85"), D("5"), Farol.verde),
        (MAIOR, MetaValores(valor=D("80")), D("80"), D("5"), Farol.verde),
        (MAIOR, MetaValores(valor=D("80")), D("77"), D("5"), Farol.amarelo),
        (MAIOR, MetaValores(valor=D("80")), D("76"), D("5"), Farol.amarelo),
        (MAIOR, MetaValores(valor=D("80")), D("75.9"), D("5"), Farol.vermelho),
        (MAIOR, MetaValores(valor=D("80")), D("79.9999"), D("0"), Farol.vermelho),
        # menor_melhor (F01 RN3, rascunho): meta 10 => amarelo até 10,5
        (MENOR, MetaValores(valor=D("10")), D("9"), D("5"), Farol.verde),
        (MENOR, MetaValores(valor=D("10")), D("10"), D("5"), Farol.verde),
        (MENOR, MetaValores(valor=D("10")), D("10.4"), D("5"), Farol.amarelo),
        (MENOR, MetaValores(valor=D("10")), D("10.5"), D("5"), Farol.amarelo),
        (MENOR, MetaValores(valor=D("10")), D("11"), D("5"), Farol.vermelho),
        # faixa (F01 RN3, rascunho): 90 a 110 => amarelo de 85,5 a 115,5
        (FAIXA, MetaValores(valor_min=D("90"), valor_max=D("110")), D("100"), D("5"), Farol.verde),
        (FAIXA, MetaValores(valor_min=D("90"), valor_max=D("110")), D("90"), D("5"), Farol.verde),
        (FAIXA, MetaValores(valor_min=D("90"), valor_max=D("110")), D("88"), D("5"), Farol.amarelo),
        (FAIXA, MetaValores(valor_min=D("90"), valor_max=D("110")), D("85.5"), D("5"), Farol.amarelo),
        (FAIXA, MetaValores(valor_min=D("90"), valor_max=D("110")), D("80"), D("5"), Farol.vermelho),
        (FAIXA, MetaValores(valor_min=D("90"), valor_max=D("110")), D("115.5"), D("5"), Farol.amarelo),
        (FAIXA, MetaValores(valor_min=D("90"), valor_max=D("110")), D("116"), D("5"), Farol.vermelho),
    ],
)
def test_calcular_farol(polaridade: Polaridade, meta: MetaValores, valor: D, tolerancia: D, esperado: Farol) -> None:
    assert calcular_farol(valor, meta, polaridade, tolerancia) == esperado


@pytest.mark.parametrize("polaridade", list(Polaridade))
def test_sem_medicao_e_sem_dado(polaridade: Polaridade) -> None:
    meta = MetaValores(valor=D("80"), valor_min=D("1"), valor_max=D("2"))
    assert calcular_farol(None, meta, polaridade, D("5")) == Farol.sem_dado


@pytest.mark.parametrize("polaridade", list(Polaridade))
def test_sem_meta_e_sem_dado(polaridade: Polaridade) -> None:
    assert calcular_farol(D("80"), None, polaridade, D("5")) == Farol.sem_dado
    assert calcular_farol(D("80"), MetaValores(), polaridade, D("5")) == Farol.sem_dado

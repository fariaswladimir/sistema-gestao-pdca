"""Cálculo do farol. Único lugar do sistema que decide verde/amarelo/vermelho/sem_dado."""

from dataclasses import dataclass
from decimal import Decimal

from app.dominio.tipos import Farol, Polaridade

CEM = Decimal("100")


@dataclass(frozen=True)
class MetaValores:
    valor: Decimal | None = None
    valor_min: Decimal | None = None
    valor_max: Decimal | None = None


def calcular_farol(
    valor: Decimal | None, meta: MetaValores | None, polaridade: Polaridade, tolerancia_pct: Decimal
) -> Farol:
    """Limites inclusivos: valor exatamente no limite da tolerância ainda é amarelo."""
    if valor is None or meta is None:
        return Farol.sem_dado
    tol = tolerancia_pct / CEM
    match polaridade:
        case Polaridade.maior_melhor:
            if meta.valor is None:
                return Farol.sem_dado
            return _classificar(valor >= meta.valor, valor >= meta.valor * (1 - tol))
        case Polaridade.menor_melhor:
            if meta.valor is None:
                return Farol.sem_dado
            return _classificar(valor <= meta.valor, valor <= meta.valor * (1 + tol))
        case Polaridade.faixa:
            if meta.valor_min is None or meta.valor_max is None:
                return Farol.sem_dado
            return _classificar(
                meta.valor_min <= valor <= meta.valor_max,
                meta.valor_min * (1 - tol) <= valor <= meta.valor_max * (1 + tol),
            )


def _classificar(no_alvo: bool, na_tolerancia: bool) -> Farol:
    if no_alvo:
        return Farol.verde
    return Farol.amarelo if na_tolerancia else Farol.vermelho

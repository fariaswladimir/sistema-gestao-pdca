from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, PlainSerializer

from app.dominio.tipos import Farol, Polaridade

# Decimal internamente (sem erro de arredondamento); número no JSON.
Numero = Annotated[Decimal, PlainSerializer(float, return_type=float, when_used="json")]


class MetaSaida(BaseModel):
    valor: Numero | None
    valor_min: Numero | None
    valor_max: Numero | None


class IndicadorResumo(BaseModel):
    id: UUID
    codigo: str
    nome: str
    unidade: str
    polaridade: Polaridade
    periodo: str = Field(description="Período atual, AAAA-MM")
    meta: MetaSaida | None
    valor: Numero | None
    farol: Farol


class MedicaoSaida(BaseModel):
    periodo: str
    valor: Numero
    farol: Farol
    justificativa_correcao: str | None


class IndicadorDetalhe(IndicadorResumo):
    tolerancia_pct: Numero
    medicoes: list[MedicaoSaida] = Field(description="Últimos 12 períodos com medição, do mais recente ao mais antigo")


class MedicaoEntrada(BaseModel):
    valor: Decimal = Field(max_digits=18, decimal_places=4)
    justificativa: str | None = Field(default=None, max_length=1000)

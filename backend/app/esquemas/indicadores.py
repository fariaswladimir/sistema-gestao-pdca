from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, Field, PlainSerializer, WithJsonSchema

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
    medicoes: list[MedicaoSaida] = Field(
        description="Últimos 12 períodos com medição, do mais recente ao mais antigo"
    )


# NUMERIC(18,4): até 14 dígitos inteiros; casas além da 4ª são arredondadas (meio para cima).
LIMITE_VALOR = Decimal("99999999999999")


def _quatro_casas(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


ValorMedicao = Annotated[
    Decimal,
    Field(ge=-LIMITE_VALOR, le=LIMITE_VALOR, allow_inf_nan=False),
    AfterValidator(_quatro_casas),
    WithJsonSchema(
        {
            "type": "number",
            "minimum": -int(LIMITE_VALOR),
            "maximum": int(LIMITE_VALOR),
            "description": "Valor medido; arredondado para 4 casas decimais",
        }
    ),
]


class MedicaoEntrada(BaseModel):
    valor: ValorMedicao
    justificativa: str | None = Field(default=None, max_length=1000)

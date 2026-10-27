from decimal import Decimal
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracao(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    database_url: str = "postgresql+asyncpg://gestao:gestao_dev@localhost:5432/gestao"
    oidc_issuer: str = "http://localhost:8080/realms/gestao"
    oidc_jwks_url: str = "http://localhost:8080/realms/gestao/protocol/openid-connect/certs"
    oidc_audience: str = "gestao-api"
    tz_regras: str = "America/Recife"
    tolerancia_padrao_pct: Decimal = Decimal("5")
    app_version: str = "dev"
    log_json: bool = True


@lru_cache
def obter_configuracao() -> Configuracao:
    return Configuracao()

"""Banco de testes: Postgres real (TEST_DATABASE_URL no CI, Testcontainers localmente)."""

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, text

RAIZ_BACKEND = Path(__file__).resolve().parents[1]
IMAGEM_POSTGRES = "pgvector/pgvector:pg16"


def url_async(url: str) -> str:
    return url.replace("postgresql+psycopg://", "postgresql+asyncpg://")


def url_sync(url: str) -> str:
    return url.replace("postgresql+asyncpg://", "postgresql+psycopg://")


@contextmanager
def banco_de_testes() -> Iterator[str]:
    """Devolve a URL síncrona (psycopg) de um banco vazio para a sessão de testes."""
    url = os.environ.get("TEST_DATABASE_URL")
    if url:
        yield url_sync(url)
        return
    from testcontainers.community.postgres import PostgresContainer

    with PostgresContainer(IMAGEM_POSTGRES, driver="psycopg") as pg:
        yield pg.get_connection_url()


def aplicar_migracoes(url: str, revisao: str = "head") -> None:
    cfg = Config(str(RAIZ_BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(RAIZ_BACKEND / "migrations"))
    cfg.set_main_option("sqlalchemy.url", url_async(url))
    command.upgrade(cfg, revisao)


def reverter_migracoes(url: str, revisao: str = "base") -> None:
    cfg = Config(str(RAIZ_BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(RAIZ_BACKEND / "migrations"))
    cfg.set_main_option("sqlalchemy.url", url_async(url))
    command.downgrade(cfg, revisao)


def limpar(engine: Engine) -> None:
    with engine.begin() as con:
        tabelas = con.execute(
            text("select tablename from pg_tables where schemaname = 'public' and tablename <> 'alembic_version'")
        ).scalars()
        nomes = ", ".join(f'"{t}"' for t in tabelas)
        if nomes:
            con.execute(text(f"truncate {nomes} restart identity cascade"))

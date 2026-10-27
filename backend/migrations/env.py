import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import obter_configuracao

config = context.config
if config.config_file_name and config.attributes.get("configurar_log", True):
    fileConfig(config.config_file_name, disable_existing_loggers=False)

try:
    from app.modelos import Base

    metadados = Base.metadata
except ImportError:  # antes da primeira migração
    metadados = None


def _url() -> str:
    return config.get_main_option("sqlalchemy.url") or obter_configuracao().database_url


def _rodar(con: Connection) -> None:
    context.configure(connection=con, target_metadata=metadados, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


async def _online() -> None:
    engine = create_async_engine(_url())
    async with engine.connect() as con:
        await con.run_sync(_rodar)
    await engine.dispose()


if context.is_offline_mode():
    context.configure(url=_url(), target_metadata=metadados, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    asyncio.run(_online())

from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


def criar_engine(url: str) -> AsyncEngine:
    return create_async_engine(url, pool_pre_ping=True)


def criar_fabrica(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


async def sessao_db(request: Request) -> AsyncIterator[AsyncSession]:
    fabrica: async_sessionmaker[AsyncSession] = request.app.state.fabrica_sessao
    async with fabrica() as sessao:
        yield sessao

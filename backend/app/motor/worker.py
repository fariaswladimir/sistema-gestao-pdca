"""Worker da fila (`fila_tarefa`). Vários workers podem rodar juntos: cada tarefa é travada (SKIP LOCKED)."""

import asyncio
import os
from collections.abc import Awaitable, Callable
from datetime import timedelta
from pathlib import Path
from typing import Any

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.banco import criar_engine, criar_fabrica
from app.config import obter_configuracao
from app.dominio.tipos import StatusTarefa
from app.logs import configurar_logs
from app.modelos import FilaTarefa

Tratador = Callable[[AsyncSession, dict[str, Any]], Awaitable[None]]
TRATADORES: dict[str, Tratador] = {}
MAX_TENTATIVAS = 5
# Batimento: tocado a cada volta do laço; o healthcheck do contêiner exige que seja recente.
ARQUIVO_BATIMENTO = Path(os.environ.get("WORKER_BATIMENTO", "/tmp/worker-batimento"))

log = structlog.get_logger()


def tratador(tipo: str) -> Callable[[Tratador], Tratador]:
    def registrar(funcao: Tratador) -> Tratador:
        TRATADORES[tipo] = funcao
        return funcao

    return registrar


# TODO(F03): @tratador("MedicaoRegistrada") abre anomalia em rascunho quando o farol fica vermelho.


async def processar_lote(fabrica: async_sessionmaker[AsyncSession], limite: int = 20) -> int:
    async with fabrica() as sessao, sessao.begin():
        tarefas = (
            await sessao.scalars(
                select(FilaTarefa)
                .where(FilaTarefa.status == StatusTarefa.pendente, FilaTarefa.executar_em <= func.now())
                .order_by(FilaTarefa.executar_em)
                .limit(limite)
                .with_for_update(skip_locked=True)
            )
        ).all()
        for tarefa in tarefas:
            await _executar(sessao, tarefa)
        return len(tarefas)


async def _executar(sessao: AsyncSession, tarefa: FilaTarefa) -> None:
    funcao = TRATADORES.get(tarefa.tipo)
    try:
        if funcao is None:
            log.info("tarefa_sem_tratador", tipo=tarefa.tipo, tarefa_id=str(tarefa.id))
        else:
            async with sessao.begin_nested():
                await funcao(sessao, tarefa.payload)
        tarefa.status = StatusTarefa.concluida
    except Exception:
        tarefa.tentativas += 1
        log.exception(
            "tarefa_falhou", tipo=tarefa.tipo, tarefa_id=str(tarefa.id), tentativas=tarefa.tentativas
        )
        if tarefa.tentativas >= MAX_TENTATIVAS:
            tarefa.status = StatusTarefa.falhou
        else:
            tarefa.executar_em = func.now() + timedelta(seconds=30 * 2**tarefa.tentativas)


async def rodar(intervalo_s: float = 2.0, espera_falha_s: float = 5.0) -> None:
    config = obter_configuracao()
    configurar_logs(json=config.log_json)
    engine = criar_engine(config.database_url)
    fabrica = criar_fabrica(engine)
    log.info("worker_iniciado")
    try:
        while True:
            await asyncio.to_thread(ARQUIVO_BATIMENTO.touch)
            try:
                processadas = await processar_lote(fabrica)
            except Exception:
                # Banco fora do ar ou ainda sem migração: espera e tenta de novo, sem derrubar o worker.
                log.exception("worker_ciclo_falhou")
                await asyncio.sleep(espera_falha_s)
                continue
            if processadas == 0:
                await asyncio.sleep(intervalo_s)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(rodar())

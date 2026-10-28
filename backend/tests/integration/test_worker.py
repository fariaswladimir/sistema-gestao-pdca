import asyncio
from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, text
from sqlalchemy.ext.asyncio import AsyncSession

from apoio_testes import banco, dados
from apoio_testes.tokens import cabecalho
from app.banco import criar_engine, criar_fabrica
from app.motor import worker


def _processar(url_banco: str) -> int:
    async def _rodar() -> int:
        engine = criar_engine(banco.url_async(url_banco))
        try:
            return await worker.processar_lote(criar_fabrica(engine))
        finally:
            await engine.dispose()

    return asyncio.run(_rodar())


def _tarefas(engine: Engine) -> list[Any]:
    with engine.connect() as con:
        return con.execute(text("select tipo, status, tentativas, payload from fila_tarefa")).all()


@pytest.fixture
def tratador_que_falha() -> Iterator[None]:
    async def falhar(sessao: AsyncSession, payload: dict[str, Any]) -> None:
        raise RuntimeError("falha simulada")

    worker.TRATADORES["MedicaoRegistrada"] = falhar
    yield
    worker.TRATADORES.pop("MedicaoRegistrada")


def _lancar(cliente: TestClient, engine: Engine) -> None:
    with engine.begin() as con:
        s = dados.setor(con, "Piloto")
        ind = dados.indicador(con, "IND-01", s, dados.colaborador(con, "ana", s))
    resposta = cliente.put(
        f"/indicadores/{ind}/medicoes/2026-10", json={"valor": 70}, headers=cabecalho("ana")
    )
    assert resposta.status_code == 201, resposta.text


def test_medicao_registrada_vai_ao_outbox_e_e_concluida(
    cliente: TestClient, engine: Engine, url_banco: str
) -> None:
    _lancar(cliente, engine)
    [tarefa] = _tarefas(engine)
    assert (tarefa.tipo, tarefa.status) == ("MedicaoRegistrada", "pendente")
    assert tarefa.payload["farol"] == "vermelho"
    assert _processar(url_banco) == 1
    assert _tarefas(engine)[0].status == "concluida"
    assert _processar(url_banco) == 0


def test_falha_no_tratador_reagenda_a_tarefa(
    cliente: TestClient, engine: Engine, url_banco: str, tratador_que_falha: None
) -> None:
    _lancar(cliente, engine)
    _processar(url_banco)
    [tarefa] = _tarefas(engine)
    assert (tarefa.status, tarefa.tentativas) == ("pendente", 1)
    assert _processar(url_banco) == 0  # reagendada para depois


def test_worker_sobrevive_a_banco_sem_migracao(monkeypatch: pytest.MonkeyPatch) -> None:
    """No primeiro `up`, o worker sobe antes das migrações: deve registrar o erro e continuar."""
    chamadas = 0

    async def falhar(*_: Any, **__: Any) -> int:
        nonlocal chamadas
        chamadas += 1
        if chamadas >= 3:
            raise asyncio.CancelledError
        raise RuntimeError("relation fila_tarefa does not exist")

    monkeypatch.setattr(worker, "processar_lote", falhar)
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(worker.rodar(espera_falha_s=0))
    assert chamadas == 3

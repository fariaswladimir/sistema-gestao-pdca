"""Contrato da API: Schemathesis gera requisições a partir do /openapi.json e confere as respostas."""

from collections.abc import Iterator
from typing import Any

import pytest
import schemathesis
from fastapi.testclient import TestClient
from sqlalchemy import Engine

from apoio_testes import dados
from apoio_testes.tokens import cabecalho


@pytest.fixture
def esquema_api(cliente: TestClient, engine: Engine) -> Iterator[Any]:
    with engine.begin() as con:
        s = dados.setor(con, "Piloto")
        dados.indicador(con, "IND-01", s, dados.colaborador(con, "ana", s))
    yield schemathesis.openapi.from_asgi("/openapi.json", cliente.app)


esquema = schemathesis.pytest.from_fixture("esquema_api")


@esquema.parametrize()
def test_api_cumpre_o_contrato(case: schemathesis.Case) -> None:
    case.call_and_validate(headers=cabecalho("ana"))

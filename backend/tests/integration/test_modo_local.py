"""Modo local (diretrizes de versão): usuário escolhido na entrada, sem senha e sem perfis."""

from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy import Engine, text

from apoio_testes import dados


def _piloto(engine: Engine) -> dict[str, Any]:
    with engine.begin() as con:
        s = dados.setor(con, "Piloto")
        ana = dados.colaborador(con, "ana", s)
        bruno = dados.colaborador(con, "bruno", s)
        return {"ana": ana, "ind_bruno": dados.indicador(con, "IND-02", s, bruno)}


def test_sem_usuario_escolhido_e_401(cliente_local: TestClient) -> None:
    assert cliente_local.get("/eu").status_code == 401


def test_cabecalho_invalido_ou_desconhecido_e_401(cliente_local: TestClient, engine: Engine) -> None:
    _piloto(engine)
    for valor in ("nao-e-uuid", "00000000-0000-4000-8000-000000000000"):
        assert cliente_local.get("/eu", headers={"X-Usuario-Local": valor}).status_code == 401


def test_usuario_escolhido_entra(cliente_local: TestClient, engine: Engine) -> None:
    _piloto(engine)
    resposta = cliente_local.get("/eu", headers=dados.cabecalho_local(engine, "ana"))
    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["nome"] == "Ana"


def test_colaborador_desligado_nao_entra_nem_aparece_na_lista(
    cliente_local: TestClient, engine: Engine
) -> None:
    _piloto(engine)
    with engine.begin() as con:
        con.execute(text("update colaborador set status = 'desligado' where email = 'ana@exemplo.org'"))
    assert cliente_local.get("/eu", headers=dados.cabecalho_local(engine, "ana")).status_code == 403
    nomes = {u["nome"] for u in cliente_local.get("/sessao-local/usuarios").json()}
    assert nomes == {"Bruno"}


def test_sem_perfis_qualquer_usuario_le_e_lanca_em_qualquer_indicador(
    cliente_local: TestClient, engine: Engine
) -> None:
    ids = _piloto(engine)
    ana = dados.cabecalho_local(engine, "ana")
    assert cliente_local.get(f"/indicadores/{ids['ind_bruno']}", headers=ana).status_code == 200
    resposta = cliente_local.put(
        f"/indicadores/{ids['ind_bruno']}/medicoes/2026-10", json={"valor": 81}, headers=ana
    )
    assert resposta.status_code == 201, resposta.text
    with engine.connect() as con:
        ator = con.execute(
            text("select ator_id from evento_auditoria where entidade = 'medicao'")
        ).scalar_one()
    assert ator == ids["ana"]


def test_bearer_e_ignorado_no_modo_local(cliente_local: TestClient, engine: Engine) -> None:
    _piloto(engine)
    assert cliente_local.get("/eu", headers={"Authorization": "Bearer qualquer"}).status_code == 401


def test_rota_de_escolha_nao_existe_no_modo_oidc(cliente: TestClient) -> None:
    assert cliente.get("/sessao-local/usuarios").status_code == 404

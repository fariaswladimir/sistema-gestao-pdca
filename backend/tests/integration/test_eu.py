from apoio_testes import dados
from apoio_testes.tokens import cabecalho, emitir_token
from fastapi.testclient import TestClient
from sqlalchemy import Engine, text


def _ana(engine: Engine) -> None:
    with engine.begin() as con:
        dados.colaborador(con, "ana", dados.setor(con, "Piloto"))


def test_eu_sem_token_e_401(cliente: TestClient) -> None:
    resposta = cliente.get("/eu")
    assert resposta.status_code == 401
    assert resposta.headers["www-authenticate"] == "Bearer"


def test_primeiro_acesso_vincula_sub_pelo_email(cliente: TestClient, engine: Engine) -> None:
    _ana(engine)
    resposta = cliente.get("/eu", headers=cabecalho("ana"))
    assert resposta.status_code == 200, resposta.text
    assert resposta.json()["perfil"] == "colaborador"
    with engine.connect() as con:
        assert con.execute(text("select sub_oidc from colaborador")).scalar_one() == "sub-ana"


def test_email_ja_vinculado_a_outro_sub_e_recusado(cliente: TestClient, engine: Engine) -> None:
    _ana(engine)
    assert cliente.get("/eu", headers=cabecalho("ana")).status_code == 200
    intruso = emitir_token(sub="outro-sub", email="ana@exemplo.org")
    assert cliente.get("/eu", headers={"Authorization": f"Bearer {intruso}"}).status_code == 403


def test_token_valido_sem_cadastro_e_403(cliente: TestClient, engine: Engine) -> None:
    assert cliente.get("/eu", headers=cabecalho("desconhecido")).status_code == 403


def test_colaborador_desligado_e_403(cliente: TestClient, engine: Engine) -> None:
    _ana(engine)
    with engine.begin() as con:
        con.execute(text("update colaborador set status = 'desligado'"))
    assert cliente.get("/eu", headers=cabecalho("ana")).status_code == 403

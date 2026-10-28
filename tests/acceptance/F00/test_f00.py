"""Passos da F00 – Esqueleto andante. Lê a spec aprovada direto de specs/F00-esqueleto/acceptance.feature.

Roda no modo como o produto está hoje (diretrizes de versão): usuário escolhido, sem perfis.
"""

from decimal import Decimal
from typing import Any

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when
from sqlalchemy import Engine, text

from apoio_testes import dados

scenarios("F00-esqueleto/acceptance.feature")


class Contexto:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self.indicadores: dict[str, Any] = {}
        self.login: str | None = None
        self.resposta: Any = None
        self.ultimo_lancamento: tuple[str, str] | None = None

    def cabecalho(self) -> dict[str, str]:
        assert self.login, "nenhum usuário autenticado no cenário"
        return dados.cabecalho_local(self.engine, self.login)


@pytest.fixture
def cliente(cliente_local: TestClient) -> TestClient:
    return cliente_local


@pytest.fixture
def ctx(engine: Engine) -> Contexto:
    return Contexto(engine)


def _lancar(
    cliente: TestClient, ctx: Contexto, codigo: str, periodo: str, valor: str, justificativa: str | None
):
    assert ctx.login, "nenhum usuário autenticado no cenário"
    corpo: dict[str, Any] = {"valor": valor}
    if justificativa is not None:
        corpo["justificativa"] = justificativa
    ctx.ultimo_lancamento = (codigo, periodo)
    ctx.resposta = cliente.put(
        f"/indicadores/{ctx.indicadores[codigo]}/medicoes/{periodo}", json=corpo, headers=ctx.cabecalho()
    )
    return ctx.resposta


# Contexto ---------------------------------------------------------------------------------------


@given(parsers.parse('o setor "{setor}" com o colaborador "{login}" responsável pelo indicador "{codigo}"'))
def setor_colaborador_indicador(engine: Engine, ctx: Contexto, setor: str, login: str, codigo: str) -> None:
    with engine.begin() as con:
        s = dados.setor(con, setor)
        c = dados.colaborador(con, login, s)
        ctx.indicadores[codigo] = dados.indicador(con, codigo, s, c)


@given(parsers.parse('o indicador "{codigo}" é "{polaridade}" com meta {meta} e tolerância {tol}%'))
def configurar_indicador(engine: Engine, codigo: str, polaridade: str, meta: str, tol: str) -> None:
    with engine.begin() as con:
        dados.configurar_indicador(con, codigo, polaridade, Decimal(meta), Decimal(tol))


@given(parsers.parse('o indicador "{codigo}" sob responsabilidade de "{login}"'))
def indicador_de_outro(engine: Engine, ctx: Contexto, codigo: str, login: str) -> None:
    with engine.begin() as con:
        s = dados.setor(con, "Outro")
        c = dados.colaborador(con, login, s)
        ctx.indicadores[codigo] = dados.indicador(con, codigo, s, c)


@given(parsers.parse('"{login}" está autenticada'))
def autenticada(ctx: Contexto, login: str) -> None:
    ctx.login = login


@given(parsers.parse('"{login}" lançou {valor} em "{codigo}" no período "{periodo}"'))
def ja_lancou(cliente: TestClient, ctx: Contexto, login: str, valor: str, codigo: str, periodo: str) -> None:
    ctx.login = login
    assert _lancar(cliente, ctx, codigo, periodo, valor, None).status_code == 201


# Ações ------------------------------------------------------------------------------------------


@when("um visitante sem sessão acessa a lista de indicadores")
def visitante_lista(cliente: TestClient, ctx: Contexto) -> None:
    ctx.resposta = cliente.get("/indicadores/meus")


@when("um visitante abre a escolha de usuário")
def visitante_escolha(cliente: TestClient, ctx: Contexto) -> None:
    ctx.resposta = cliente.get("/sessao-local/usuarios")


@when("um visitante consulta a saúde do sistema")
def visitante_saude(cliente: TestClient, ctx: Contexto) -> None:
    ctx.resposta = cliente.get("/saude")


@when("ela consulta seus indicadores")
def consulta_meus(cliente: TestClient, ctx: Contexto) -> None:
    assert ctx.login
    ctx.resposta = cliente.get("/indicadores/meus", headers=ctx.cabecalho())


@when(parsers.parse('ela lança o valor {valor} em "{codigo}" no período "{periodo}"'))
def lanca_valor(cliente: TestClient, ctx: Contexto, valor: str, codigo: str, periodo: str) -> None:
    resposta = _lancar(cliente, ctx, codigo, periodo, valor, None)
    assert resposta.status_code in (200, 201), resposta.text


@when(parsers.parse("ela lança {valor} no mesmo período sem justificativa"))
def relanca_sem(cliente: TestClient, ctx: Contexto, valor: str) -> None:
    assert ctx.ultimo_lancamento
    _lancar(cliente, ctx, *ctx.ultimo_lancamento, valor, None)


@when(parsers.parse('ela lança {valor} no mesmo período com justificativa "{justificativa}"'))
def relanca_com(cliente: TestClient, ctx: Contexto, valor: str, justificativa: str) -> None:
    assert ctx.ultimo_lancamento
    _lancar(cliente, ctx, *ctx.ultimo_lancamento, valor, justificativa)


# Verificações -----------------------------------------------------------------------------------


@then(parsers.parse("recebe resposta {codigo:d}"))
def recebe_resposta(ctx: Contexto, codigo: int) -> None:
    assert ctx.resposta.status_code == codigo, ctx.resposta.text
    if codigo >= 400:
        assert ctx.resposta.json()["codigo"]


@then(parsers.parse('recebe resposta {codigo:d} com status "{status}" e versão'))
def recebe_saude(ctx: Contexto, codigo: int, status: str) -> None:
    assert ctx.resposta.status_code == codigo, ctx.resposta.text
    if codigo >= 400:
        assert ctx.resposta.json()["codigo"]
    corpo = ctx.resposta.json()
    assert corpo["status"] == status
    assert corpo["versao"]


@then(parsers.parse('vê "{codigo}" com farol "{farol}" no período atual'))
def ve_farol_atual(ctx: Contexto, codigo: str, farol: str) -> None:
    assert ctx.resposta.status_code == 200, ctx.resposta.text
    itens = {i["codigo"]: i for i in ctx.resposta.json()}
    assert codigo in itens
    assert itens[codigo]["periodo"] == "2026-10"
    assert itens[codigo]["farol"] == farol


@then(parsers.parse('vê "{visivel}" e não vê "{oculto}"'))
def ve_so_os_seus(ctx: Contexto, visivel: str, oculto: str) -> None:
    assert ctx.resposta.status_code == 200, ctx.resposta.text
    codigos = {i["codigo"] for i in ctx.resposta.json()}
    assert visivel in codigos
    assert oculto not in codigos


@then(parsers.parse('vê "{nome}" na lista, sem e-mail'))
def ve_na_escolha(ctx: Contexto, nome: str) -> None:
    assert ctx.resposta.status_code == 200, ctx.resposta.text
    usuarios = ctx.resposta.json()
    assert nome in {u["nome"] for u in usuarios}
    assert all("email" not in u for u in usuarios)


@then(parsers.parse('o farol de "{codigo}" em "{periodo}" é "{farol}"'))
def farol_no_periodo(cliente: TestClient, ctx: Contexto, codigo: str, periodo: str, farol: str) -> None:
    assert ctx.login
    resposta = cliente.get(f"/indicadores/{ctx.indicadores[codigo]}", headers=ctx.cabecalho())
    assert resposta.status_code == 200, resposta.text
    medicoes = {m["periodo"]: m for m in resposta.json()["medicoes"]}
    assert medicoes[periodo]["farol"] == farol


@then(parsers.parse('o farol passa a "{farol}"'))
def farol_passa(ctx: Contexto, farol: str) -> None:
    assert ctx.resposta.status_code == 200, ctx.resposta.text
    assert ctx.resposta.json()["farol"] == farol


@then(parsers.parse("existe evento de auditoria da medição com valor anterior {antes} e novo {depois}"))
def auditoria_medicao(engine: Engine, antes: str, depois: str) -> None:
    with engine.connect() as con:
        eventos = con.execute(
            text("select antes, depois, ator_tipo, canal from evento_auditoria where entidade = 'medicao'")
        ).all()
    correcoes = [e for e in eventos if e.antes is not None]
    assert len(correcoes) == 1
    e = correcoes[0]
    assert Decimal(e.antes["valor"]) == Decimal(antes)
    assert Decimal(e.depois["valor"]) == Decimal(depois)
    assert e.ator_tipo == "humano"
    assert e.canal == "web"

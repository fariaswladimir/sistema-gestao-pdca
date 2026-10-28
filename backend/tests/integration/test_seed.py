import asyncio

from apoio_testes import banco
from sqlalchemy import Engine, text

from app.seed import semear


def _contar(engine: Engine) -> dict[str, int]:
    with engine.connect() as con:
        return {
            t: con.execute(text(f"select count(*) from {t}")).scalar_one()
            for t in ("setor", "colaborador", "ciclo", "tipo_indicador", "indicador", "meta")
        }


def test_seed_e_idempotente(url_banco: str, engine: Engine) -> None:
    asyncio.run(semear(banco.url_async(url_banco)))
    primeira = _contar(engine)
    asyncio.run(semear(banco.url_async(url_banco)))
    assert _contar(engine) == primeira
    assert primeira == {
        "setor": 3,
        "colaborador": 6,
        "ciclo": 1,
        "tipo_indicador": 1,
        "indicador": 2,
        "meta": 2,
    }


def test_seed_espelha_usuarios_do_keycloak(url_banco: str, engine: Engine) -> None:
    import json

    realm = json.loads((banco.RAIZ_BACKEND.parent / "infra/keycloak/realm-gestao.json").read_text("utf-8"))
    asyncio.run(semear(banco.url_async(url_banco)))
    with engine.connect() as con:
        emails = set(con.execute(text("select email from colaborador")).scalars())
    assert emails == {u["email"] for u in realm["users"]}

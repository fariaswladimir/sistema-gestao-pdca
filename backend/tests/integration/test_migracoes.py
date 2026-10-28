from sqlalchemy import Engine, inspect, text

from apoio_testes import banco

TABELAS_F00 = {
    "setor",
    "colaborador",
    "ciclo",
    "tipo_indicador",
    "indicador",
    "meta",
    "medicao",
    "evento_auditoria",
    "fila_tarefa",
}


def _tabelas(engine: Engine) -> set[str]:
    return set(inspect(engine).get_table_names()) - {"alembic_version"}


def test_migracao_cria_tabelas_e_extensoes(engine: Engine) -> None:
    assert _tabelas(engine) >= TABELAS_F00
    with engine.connect() as con:
        extensoes = set(con.execute(text("select extname from pg_extension")).scalars())
    assert {"ltree", "vector"} <= extensoes


def test_migracao_desce_e_sobe(url_banco: str, engine: Engine) -> None:
    banco.reverter_migracoes(url_banco)
    engine.dispose()
    assert _tabelas(engine) == set()
    banco.aplicar_migracoes(url_banco)
    engine.dispose()
    assert _tabelas(engine) >= TABELAS_F00

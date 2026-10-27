"""Montagem de dados de teste direto no banco (caixa-preta em relação ao código da aplicação)."""

from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import Connection, text
from uuid6 import uuid7


def _inserir(con: Connection, tabela: str, **valores: Any) -> Any:
    valores.setdefault("id", uuid7())
    colunas = ", ".join(valores)
    params = ", ".join(f":{c}" for c in valores)
    con.execute(text(f"insert into {tabela} ({colunas}) values ({params})"), valores)
    return valores["id"]


def setor(con: Connection, nome: str) -> Any:
    existente = con.execute(text("select id from setor where nome = :n"), {"n": nome}).scalar()
    return existente or _inserir(con, "setor", nome=nome, sigla=nome[:3].upper(), ativo=True)


def colaborador(con: Connection, login: str, setor_id: Any, perfil: str = "colaborador") -> Any:
    email = f"{login}@exemplo.org"
    existente = con.execute(text("select id from colaborador where email = :e"), {"e": email}).scalar()
    return existente or _inserir(
        con, "colaborador", nome=login.capitalize(), email=email, setor_id=setor_id, perfil=perfil, status="ativo"
    )


def ciclo(con: Connection, ano: int = 2026) -> Any:
    existente = con.execute(text("select id from ciclo where nome = :n"), {"n": str(ano)}).scalar()
    return existente or _inserir(
        con, "ciclo", nome=str(ano), inicio=date(ano, 1, 1), fim=date(ano, 12, 31), status="vigente"
    )


def tipo_indicador(con: Connection, polaridade: str) -> Any:
    nome = f"Setor {polaridade}"
    existente = con.execute(text("select id from tipo_indicador where nome = :n"), {"n": nome}).scalar()
    return existente or _inserir(
        con,
        "tipo_indicador",
        nome=nome,
        nivel="setor",
        natureza="controle",
        polaridade=polaridade,
        consolidacao="nenhuma",
        origem="manual",
    )


def indicador(
    con: Connection,
    codigo: str,
    setor_id: Any,
    responsavel_id: Any,
    *,
    polaridade: str = "maior_melhor",
    meta: Decimal = Decimal("80"),
    tolerancia_pct: Decimal = Decimal("5"),
) -> Any:
    ind = _inserir(
        con,
        "indicador",
        codigo=codigo,
        nome=f"Indicador {codigo}",
        tipo_id=tipo_indicador(con, polaridade),
        setor_id=setor_id,
        responsavel_id=responsavel_id,
        unidade="%",
        periodicidade="mensal",
        tolerancia_pct=tolerancia_pct,
        ativo=True,
    )
    _inserir(con, "meta", indicador_id=ind, ciclo_id=ciclo(con), periodo=None, valor=meta)
    return ind


def configurar_indicador(
    con: Connection, codigo: str, polaridade: str, meta: Decimal, tolerancia_pct: Decimal
) -> None:
    ind = con.execute(text("select id from indicador where codigo = :c"), {"c": codigo}).scalar_one()
    con.execute(
        text("update indicador set tipo_id = :t, tolerancia_pct = :tol where id = :i"),
        {"t": tipo_indicador(con, polaridade), "tol": tolerancia_pct, "i": ind},
    )
    con.execute(text("update meta set valor = :v where indicador_id = :i"), {"v": meta, "i": ind})

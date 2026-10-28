from pathlib import Path
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest
import yaml

from app.dominio.erros import SemPermissao
from app.dominio.tipos import Perfil
from app.seguranca.autenticacao import Usuario
from app.seguranca.permissoes import PERMISSOES, exigir_permissao

MATRIZ_YAML = Path(__file__).resolve().parents[3] / "tests/permissions/matriz.yaml"
DOC = Path(__file__).resolve().parents[3] / "specs/_perfis-permissoes.md"

pytestmark = pytest.mark.anyio


def test_permissoes_py_igual_a_matriz_yaml() -> None:
    matriz = yaml.safe_load(MATRIZ_YAML.read_text("utf-8"))
    codigo = {acao: {p.value: a.value for p, a in perfis.items()} for acao, perfis in PERMISSOES.items()}
    assert codigo == matriz


def test_matriz_cobre_todas_as_acoes_do_documento() -> None:
    linhas = [
        linha for linha in DOC.read_text("utf-8").splitlines() if linha.startswith("| ") and ":" in linha
    ]
    acoes_doc = {linha.split("|")[1].strip() for linha in linhas}
    assert acoes_doc == set(PERMISSOES)


def _usuario(perfil: Perfil) -> Usuario:
    return Usuario(id=uuid4(), nome="x", perfil=perfil, setor_id=uuid4())


def _requisicao(perfis_ativos: bool) -> Any:
    return SimpleNamespace(
        app=SimpleNamespace(state=SimpleNamespace(config=SimpleNamespace(perfis_ativos=perfis_ativos)))
    )


async def test_exigir_permissao_barra_perfil_negado() -> None:
    verificar = exigir_permissao("medicao:registrar")
    with pytest.raises(SemPermissao):
        await verificar(_requisicao(True), _usuario(Perfil.leitor))


@pytest.mark.parametrize("perfil", [Perfil.colaborador, Perfil.gestor, Perfil.escritorio, Perfil.servico])
async def test_exigir_permissao_deixa_passar_perfil_permitido(perfil: Perfil) -> None:
    usuario = _usuario(perfil)
    assert await exigir_permissao("medicao:registrar")(_requisicao(True), usuario) is usuario


async def test_sem_perfis_ativos_qualquer_perfil_passa() -> None:
    usuario = _usuario(Perfil.leitor)
    assert await exigir_permissao("medicao:registrar")(_requisicao(False), usuario) is usuario


def test_acao_desconhecida_falha_cedo() -> None:
    with pytest.raises(ValueError):
        exigir_permissao("medicao:apagar")

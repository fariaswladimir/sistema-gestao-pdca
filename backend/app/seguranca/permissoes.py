"""Matriz perfil × ação. Espelha specs/_perfis-permissoes.md e tests/permissions/matriz.yaml (teste de paridade).

Letras na ordem das colunas: admin, escritorio, diretoria, gestor, colaborador, leitor, servico.
P permitido · N negado · R só rascunho · O só os próprios itens.
"""

from collections.abc import Awaitable, Callable
from enum import StrEnum

from fastapi import Depends
from sqlalchemy import ColumnElement

from app.dominio.erros import SemPermissao
from app.dominio.tipos import Perfil
from app.modelos import Indicador
from app.seguranca.autenticacao import Usuario, usuario_atual


class Acesso(StrEnum):
    permitido = "permitido"
    negado = "negado"
    rascunho = "rascunho"
    proprias = "proprias"


_ORDEM = [Perfil.admin, Perfil.escritorio, Perfil.diretoria, Perfil.gestor, Perfil.colaborador, Perfil.leitor, Perfil.servico]
_LETRAS = {"P": Acesso.permitido, "N": Acesso.negado, "R": Acesso.rascunho, "O": Acesso.proprias}

_MATRIZ = {
    "setor:gerir": "PPNNNNN",
    "colaborador:gerir": "PPNNNNN",
    "tipo_indicador:gerir": "NPNNNNN",
    "objetivo:gerir": "NPPNNNN",
    "indicador:criar_estrategico": "NPPNNNN",
    "indicador:desdobrar": "NPPPNNN",
    "indicador:ler": "PPPPPPP",
    "meta:aceitar": "NNPPPNN",
    "medicao:registrar": "NPNPPNP",
    "anomalia:criar": "NPNPPNR",
    "anomalia:editar": "NPNPPNR",
    "anomalia:aprovar": "NPNPNNN",
    "plano:gerir": "NPNPNNR",
    "acao:atualizar": "NPNPONN",
    "padrao:gerir": "NPNPNNR",
    "dto:registrar": "NPNPNNN",
    "ritual:conduzir": "NPPPNNR",
    "diagnostico:avaliar": "NPNNNNN",
    "diagnostico:ler": "PPPPPNP",
    "integracao:gerir": "PNNNNNN",
    "credencial_api:gerir": "PNNNNNN",
    "auditoria:ler": "PPPNNNN",
    "painel:ler": "PPPPPPP",
}

PERMISSOES: dict[str, dict[Perfil, Acesso]] = {
    acao: {perfil: _LETRAS[letra] for perfil, letra in zip(_ORDEM, letras, strict=True)}
    for acao, letras in _MATRIZ.items()
}


def acesso(perfil: Perfil, acao: str) -> Acesso:
    return PERMISSOES[acao][perfil]


def exigir_permissao(acao: str) -> Callable[..., Awaitable[Usuario]]:
    """Dependência FastAPI: autentica e barra o perfil sem a ação (403).

    `rascunho` e `proprias` passam aqui; o serviço aplica a restrição fina.
    """
    if acao not in PERMISSOES:
        raise ValueError(f"Ação desconhecida: {acao}")

    async def _verificar(usuario: Usuario = Depends(usuario_atual)) -> Usuario:
        if acesso(usuario.perfil, acao) == Acesso.negado:
            raise SemPermissao("Seu perfil não permite esta ação.")
        return usuario

    _verificar.acao = acao  # type: ignore[attr-defined]  # lido pelo gerador da matriz de testes
    return _verificar


def escopo_indicadores(usuario: Usuario) -> ColumnElement[bool]:
    """Indicadores visíveis ao usuário. F00 (RN2): só aqueles de que é responsável."""
    # TODO(F01): setor próprio e descendentes + estratégicos publicados; diretoria/escritório/admin veem tudo.
    return Indicador.responsavel_id == usuario.id

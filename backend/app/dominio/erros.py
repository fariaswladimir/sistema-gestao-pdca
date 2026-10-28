"""Exceções de domínio. Um único handler na API as converte em HTTP."""


class ErroDominio(Exception):
    status_http = 400
    codigo = "erro"

    def __init__(self, mensagem: str) -> None:
        super().__init__(mensagem)
        self.mensagem = mensagem


class NaoAutenticado(ErroDominio):
    status_http = 401
    codigo = "nao_autenticado"


class SemPermissao(ErroDominio):
    status_http = 403
    codigo = "sem_permissao"


class NaoEncontrado(ErroDominio):
    """Também usado para recurso fora do escopo: não revelar que existe."""

    status_http = 404
    codigo = "nao_encontrado"


class Conflito(ErroDominio):
    status_http = 409
    codigo = "conflito"


class EntradaInvalida(ErroDominio):
    status_http = 422
    codigo = "entrada_invalida"


class JustificativaObrigatoria(EntradaInvalida):
    codigo = "justificativa_obrigatoria"

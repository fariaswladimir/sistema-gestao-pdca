"""Exceções de domínio. Um único handler na API as converte em HTTP."""


class ErroDominio(Exception):
    status_http = 400

    def __init__(self, mensagem: str) -> None:
        super().__init__(mensagem)
        self.mensagem = mensagem


class NaoAutenticado(ErroDominio):
    status_http = 401


class SemPermissao(ErroDominio):
    status_http = 403


class NaoEncontrado(ErroDominio):
    """Também usado para recurso fora do escopo: não revelar que existe."""

    status_http = 404


class EntradaInvalida(ErroDominio):
    status_http = 422


class JustificativaObrigatoria(EntradaInvalida):
    pass

from app.dominio.erros import JustificativaObrigatoria


def exigir_justificativa_se_relancamento(ja_existe: bool, justificativa: str | None) -> str | None:
    """RN3: relançar o mesmo período substitui o valor e exige justificativa."""
    texto = (justificativa or "").strip() or None
    if ja_existe and texto is None:
        raise JustificativaObrigatoria("Já existe valor neste período; informe a justificativa da correção.")
    return texto if ja_existe else None

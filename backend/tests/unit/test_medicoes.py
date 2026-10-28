import pytest

from app.dominio.erros import JustificativaObrigatoria
from app.dominio.medicoes import exigir_justificativa_se_relancamento


def test_primeiro_lancamento_dispensa_e_ignora_justificativa() -> None:
    assert exigir_justificativa_se_relancamento(False, None) is None
    assert exigir_justificativa_se_relancamento(False, "qualquer") is None


@pytest.mark.parametrize("justificativa", [None, "", "   "])
def test_relancamento_sem_justificativa_e_recusado(justificativa: str | None) -> None:
    with pytest.raises(JustificativaObrigatoria):
        exigir_justificativa_se_relancamento(True, justificativa)


def test_relancamento_com_justificativa() -> None:
    assert exigir_justificativa_se_relancamento(True, "  erro de digitação ") == "erro de digitação"

from collections.abc import Iterable
from datetime import date

from app.motor.farol import MetaValores


def meta_vigente(metas: Iterable[tuple[date | None, MetaValores]], periodo: date) -> MetaValores | None:
    """Entre as metas do ciclo que contém o período, a do período prevalece sobre a do ciclo (None)."""
    do_ciclo = None
    for periodo_meta, valores in metas:
        if periodo_meta == periodo:
            return valores
        if periodo_meta is None:
            do_ciclo = valores
    return do_ciclo

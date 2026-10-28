from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auditoria import registrar_auditoria
from app.config import Configuracao
from app.dominio import periodo as periodos
from app.dominio.erros import Conflito, EntradaInvalida
from app.dominio.medicoes import exigir_justificativa_se_relancamento
from app.dominio.tipos import Canal, Origem, Polaridade
from app.esquemas.indicadores import MedicaoEntrada, MedicaoSaida
from app.modelos import Medicao
from app.motor.eventos import MedicaoRegistrada, publicar
from app.motor.farol import calcular_farol
from app.relogio import Relogio
from app.seguranca.autenticacao import Usuario
from app.servicos.indicadores import ServicoIndicadores


def _retrato(m: Medicao) -> dict[str, str | None]:
    return {
        "periodo": periodos.para_texto(m.periodo),
        "valor": f"{m.valor:f}",
        "farol": m.farol.value,
        "justificativa_correcao": m.justificativa_correcao,
    }


class ServicoMedicoes:
    def __init__(self, sessao: AsyncSession, usuario: Usuario, relogio: Relogio, config: Configuracao) -> None:
        self.sessao = sessao
        self.usuario = usuario
        self.indicadores = ServicoIndicadores(sessao, usuario, relogio, config)

    async def registrar(self, indicador_id: UUID, periodo_texto: str, entrada: MedicaoEntrada) -> tuple[MedicaoSaida, bool]:
        """Cria ou substitui a medição do período. Devolve (medição, criada?)."""
        periodo = periodos.de_texto(periodo_texto)
        indicador, polaridade = await self.indicadores.obter_visivel(indicador_id)
        if polaridade != Polaridade.maior_melhor:  # TODO(F01): liberar menor_melhor e faixa
            raise EntradaInvalida("Nesta versão só indicadores 'maior é melhor' aceitam lançamento.")

        meta = await self.indicadores.meta_do_periodo(indicador.id, periodo)
        farol = calcular_farol(entrada.valor, meta, polaridade, indicador.tolerancia_pct)
        existente = await self.sessao.scalar(
            select(Medicao).where(Medicao.indicador_id == indicador.id, Medicao.periodo == periodo).with_for_update()
        )
        justificativa = exigir_justificativa_se_relancamento(existente is not None, entrada.justificativa)

        if existente is None:
            medicao = Medicao(
                indicador_id=indicador.id,
                periodo=periodo,
                valor=entrada.valor,
                origem=Origem.manual,
                registrado_por=self.usuario.id,
                farol=farol,
            )
            self.sessao.add(medicao)
            antes, farol_anterior = None, None
        else:
            medicao = existente
            antes, farol_anterior = _retrato(existente), existente.farol.value
            medicao.valor = entrada.valor
            medicao.farol = farol
            medicao.registrado_por = self.usuario.id
            medicao.justificativa_correcao = justificativa

        try:
            await self.sessao.flush()
        except IntegrityError as erro:  # lançamento simultâneo no mesmo período
            raise Conflito("Outro lançamento para este período acabou de ser gravado; recarregue.") from erro

        registrar_auditoria(
            self.sessao,
            entidade="medicao",
            entidade_id=medicao.id,
            acao="criar" if antes is None else "substituir",
            antes=antes,
            depois=_retrato(medicao),
            ator=self.usuario,
            canal=Canal.web,  # TODO(F06): canal api para credenciais de serviço
        )
        publicar(
            self.sessao,
            MedicaoRegistrada(
                indicador_id=str(indicador.id),
                periodo=periodos.para_texto(periodo),
                valor=f"{medicao.valor:f}",
                farol=farol.value,
                farol_anterior=farol_anterior,
            ),
        )
        await self.sessao.commit()
        saida = MedicaoSaida(
            periodo=periodos.para_texto(periodo),
            valor=medicao.valor,
            farol=medicao.farol,
            justificativa_correcao=medicao.justificativa_correcao,
        )
        return saida, antes is None

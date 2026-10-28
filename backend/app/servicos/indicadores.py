from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Configuracao
from app.dominio import periodo as periodos
from app.dominio.erros import NaoEncontrado
from app.dominio.metas import meta_vigente
from app.dominio.tipos import Farol, Polaridade
from app.esquemas.indicadores import IndicadorDetalhe, IndicadorResumo, MedicaoSaida, MetaSaida
from app.modelos import Ciclo, Indicador, Medicao, Meta, TipoIndicador
from app.motor.farol import MetaValores
from app.relogio import Relogio
from app.seguranca.autenticacao import Usuario
from app.seguranca.permissoes import escopo_indicadores


class ServicoIndicadores:
    def __init__(
        self, sessao: AsyncSession, usuario: Usuario, relogio: Relogio, config: Configuracao
    ) -> None:
        self.sessao = sessao
        self.usuario = usuario
        self.periodo_atual = periodos.atual(relogio.agora(), config.tz_regras)

    async def listar_meus(self) -> list[IndicadorResumo]:
        linhas = await self.sessao.execute(
            select(Indicador, TipoIndicador.polaridade)
            .join(TipoIndicador)
            .where(escopo_indicadores(self.usuario), Indicador.ativo)
            .order_by(Indicador.codigo)
        )
        return [await self._resumo(ind, pol) for ind, pol in linhas.all()]

    async def detalhar(self, indicador_id: UUID) -> IndicadorDetalhe:
        indicador, polaridade = await self.obter_visivel(indicador_id)
        resumo = await self._resumo(indicador, polaridade)
        medicoes = await self.sessao.scalars(
            select(Medicao)
            .where(Medicao.indicador_id == indicador.id)
            .order_by(Medicao.periodo.desc())
            .limit(12)
        )
        return IndicadorDetalhe(
            **resumo.model_dump(),
            tolerancia_pct=indicador.tolerancia_pct,
            medicoes=[
                MedicaoSaida(
                    periodo=periodos.para_texto(m.periodo),
                    valor=m.valor,
                    farol=m.farol,
                    justificativa_correcao=m.justificativa_correcao,
                )
                for m in medicoes
            ],
        )

    async def obter_visivel(self, indicador_id: UUID) -> tuple[Indicador, Polaridade]:
        """Indicador dentro do escopo do usuário; fora do escopo é 404, como se não existisse."""
        linha = (
            await self.sessao.execute(
                select(Indicador, TipoIndicador.polaridade)
                .join(TipoIndicador)
                .where(Indicador.id == indicador_id, escopo_indicadores(self.usuario), Indicador.ativo)
            )
        ).first()
        if linha is None:
            raise NaoEncontrado("Indicador não encontrado.")
        return linha[0], linha[1]

    async def meta_do_periodo(self, indicador_id: UUID, periodo: date) -> MetaValores | None:
        metas = await self.sessao.scalars(
            select(Meta)
            .join(Ciclo)
            .where(Meta.indicador_id == indicador_id, Ciclo.inicio <= periodo, Ciclo.fim >= periodo)
        )
        return meta_vigente(
            ((m.periodo, MetaValores(m.valor, m.valor_min, m.valor_max)) for m in metas), periodo
        )

    async def _resumo(self, indicador: Indicador, polaridade: Polaridade) -> IndicadorResumo:
        meta = await self.meta_do_periodo(indicador.id, self.periodo_atual)
        medicao = await self.sessao.scalar(
            select(Medicao).where(Medicao.indicador_id == indicador.id, Medicao.periodo == self.periodo_atual)
        )
        return IndicadorResumo(
            id=indicador.id,
            codigo=indicador.codigo,
            nome=indicador.nome,
            unidade=indicador.unidade,
            polaridade=polaridade,
            periodo=periodos.para_texto(self.periodo_atual),
            meta=MetaSaida(valor=meta.valor, valor_min=meta.valor_min, valor_max=meta.valor_max)
            if meta
            else None,
            valor=medicao.valor if medicao else None,
            farol=medicao.farol if medicao else Farol.sem_dado,
        )

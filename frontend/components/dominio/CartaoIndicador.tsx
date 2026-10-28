import type { IndicadorResumo } from "@/lib/api/cliente";
import { numero, periodo } from "@/lib/formato";

import { Farol } from "./Farol";
import { LancarMedicao } from "./LancarMedicao";

export function CartaoIndicador({ indicador }: { indicador: IndicadorResumo }) {
  const titulo = `titulo-${indicador.id}`;
  return (
    <article aria-labelledby={titulo} className="rounded-lg bg-superficie-elevada p-4 shadow-elevada">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div className="grid gap-1">
          <h2 id={titulo} className="text-titulo-pequeno font-semibold">
            <span className="text-texto-sutil">{indicador.codigo}</span> · {indicador.nome}
          </h2>
          <dl className="flex flex-wrap gap-x-4 gap-y-1 text-texto-sutil">
            <div className="flex gap-1">
              <dt>Meta:</dt>
              <dd className="text-texto">
                {numero(indicador.meta?.valor)} {indicador.unidade}
              </dd>
            </div>
            <div className="flex gap-1">
              <dt>Valor em {periodo(indicador.periodo)}:</dt>
              <dd data-testid="valor-atual" className="text-texto">
                {indicador.valor === null ? "sem lançamento" : `${numero(indicador.valor)} ${indicador.unidade}`}
              </dd>
            </div>
          </dl>
        </div>
        <Farol farol={indicador.farol} />
      </div>
      <LancarMedicao indicadorId={indicador.id} periodoAtual={indicador.periodo} valorAtual={indicador.valor} />
    </article>
  );
}

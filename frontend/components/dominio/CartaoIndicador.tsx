import type { IndicadorResumo } from "@/lib/api/cliente";
import { numero, periodo } from "@/lib/formato";

import { Farol } from "./Farol";
import { LancarMedicao } from "./LancarMedicao";

export function CartaoIndicador({ indicador }: { indicador: IndicadorResumo }) {
  const titulo = `titulo-${indicador.id}`;
  return (
    <article aria-labelledby={titulo} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div>
          <h2 id={titulo} className="font-semibold">
            {indicador.codigo} · {indicador.nome}
          </h2>
          <dl className="mt-1 flex gap-4 text-sm text-slate-600">
            <div className="flex gap-1">
              <dt>Meta:</dt>
              <dd>
                {numero(indicador.meta?.valor)} {indicador.unidade}
              </dd>
            </div>
            <div className="flex gap-1">
              <dt>Valor em {periodo(indicador.periodo)}:</dt>
              <dd data-testid="valor-atual">
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

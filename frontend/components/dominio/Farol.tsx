import type { Farol as TipoFarol } from "@/lib/api/cliente";

/** Farol nunca só por cor: sempre ícone e texto (acessibilidade). */
const APARENCIA: Record<TipoFarol, { icone: string; texto: string; classes: string }> = {
  verde: { icone: "✔", texto: "No alvo", classes: "bg-green-100 text-green-900 ring-green-600" },
  amarelo: { icone: "!", texto: "Atenção", classes: "bg-amber-100 text-amber-900 ring-amber-500" },
  vermelho: { icone: "✖", texto: "Fora do alvo", classes: "bg-red-100 text-red-900 ring-red-600" },
  sem_dado: { icone: "–", texto: "Sem dado", classes: "bg-slate-100 text-slate-700 ring-slate-400" },
};

export function textoFarol(farol: TipoFarol): string {
  return APARENCIA[farol].texto;
}

export function Farol({ farol }: { farol: TipoFarol }) {
  const { icone, texto, classes } = APARENCIA[farol];
  return (
    <span
      data-farol={farol}
      className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium ring-1 ${classes}`}
    >
      <span aria-hidden="true">{icone}</span>
      {texto}
    </span>
  );
}

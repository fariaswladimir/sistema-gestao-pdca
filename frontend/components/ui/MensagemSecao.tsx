import type { PapelEtiqueta } from "./Etiqueta";

const PAPEL: Record<PapelEtiqueta, { classes: string; icone: string }> = {
  sucesso: { classes: "bg-sucesso-fundo", icone: "✔" },
  alerta: { classes: "bg-alerta-fundo", icone: "!" },
  perigo: { classes: "bg-perigo-fundo", icone: "✖" },
  info: { classes: "bg-info-fundo", icone: "i" },
  neutro: { classes: "bg-neutro-fundo", icone: "•" },
};

/** Section message do ADS: aviso em bloco, com ícone, título opcional e texto. */
export function MensagemSecao({
  papel,
  titulo,
  children,
}: {
  papel: PapelEtiqueta;
  titulo?: string;
  children: React.ReactNode;
}) {
  const { classes, icone } = PAPEL[papel];
  return (
    <div role={papel === "perigo" || papel === "alerta" ? "alert" : "status"} className={`flex gap-3 rounded p-4 ${classes}`}>
      <span aria-hidden="true" className="font-bold">
        {icone}
      </span>
      <div className="grid gap-1">
        {titulo && <p className="font-semibold">{titulo}</p>}
        <div>{children}</div>
      </div>
    </div>
  );
}

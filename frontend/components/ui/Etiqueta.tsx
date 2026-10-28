/**
 * Lozenge do ADS: status curto, não interativo, em caixa de frase.
 * Nunca só por cor: quem usa passa um texto claro (e, se houver, um ícone).
 */
export type PapelEtiqueta = "sucesso" | "alerta" | "perigo" | "info" | "neutro";

const PAPEL: Record<PapelEtiqueta, string> = {
  sucesso: "bg-sucesso-fundo text-sucesso-texto",
  alerta: "bg-alerta-fundo text-alerta-texto",
  perigo: "bg-perigo-fundo text-perigo-texto",
  info: "bg-info-fundo text-info-texto",
  neutro: "bg-neutro-fundo text-neutro-texto",
};

type Props = {
  papel: PapelEtiqueta;
  icone?: string;
  children: React.ReactNode;
} & React.HTMLAttributes<HTMLSpanElement>;

export function Etiqueta({ papel, icone, children, className = "", ...props }: Props) {
  return (
    <span
      className={`inline-flex max-w-52 items-center gap-1 truncate rounded px-1.5 py-0.5 text-corpo-pequeno font-semibold ${PAPEL[papel]} ${className}`}
      {...props}
    >
      {icone && <span aria-hidden="true">{icone}</span>}
      {children}
    </span>
  );
}

import type { ButtonHTMLAttributes } from "react";

/** Aparências do Button do ADS: primária (uma por tela), padrão, sutil e perigo. */
export type AparenciaBotao = "primaria" | "padrao" | "sutil" | "perigo";

const APARENCIA: Record<AparenciaBotao, string> = {
  primaria: "bg-fundo-marca text-texto-inverso hover:bg-fundo-marca-hover",
  padrao: "bg-fundo-neutro text-texto hover:bg-fundo-neutro-hover",
  sutil: "bg-transparent text-texto-sutil hover:bg-fundo-neutro hover:text-texto",
  perigo: "bg-perigo-borda text-texto-inverso hover:opacity-90",
};

export const CLASSE_FOCO =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-borda-foco";

export function classesBotao(aparencia: AparenciaBotao = "padrao") {
  return `inline-flex h-8 items-center justify-center gap-1 rounded px-3 text-corpo font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-40 ${CLASSE_FOCO} ${APARENCIA[aparencia]}`;
}

type Props = ButtonHTMLAttributes<HTMLButtonElement> & { aparencia?: AparenciaBotao };

export function Botao({ aparencia = "padrao", className = "", type = "button", ...props }: Props) {
  return <button type={type} className={`${classesBotao(aparencia)} ${className}`} {...props} />;
}

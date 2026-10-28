import type { InputHTMLAttributes } from "react";

import { CLASSE_FOCO } from "./Botao";

/** Text field do ADS: rótulo acima, borda de 2 px que vira cor de foco, mensagem de ajuda opcional. */
export const CLASSE_ENTRADA = `h-8 rounded border-2 border-borda bg-superficie px-2 text-corpo text-texto hover:border-borda-forte focus:border-borda-foco focus:outline-none ${CLASSE_FOCO}`;

type Props = InputHTMLAttributes<HTMLInputElement> & { rotulo: string; id: string; ajuda?: string };

export function Campo({ rotulo, id, ajuda, className = "", ...props }: Props) {
  return (
    <div className="grid gap-1">
      <label htmlFor={id} className="text-corpo-pequeno font-semibold text-texto-sutil">
        {rotulo}
      </label>
      <input id={id} className={`${CLASSE_ENTRADA} ${className}`} {...props} />
      {ajuda && <p className="text-corpo-pequeno text-texto-mais-sutil">{ajuda}</p>}
    </div>
  );
}

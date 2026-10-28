import { Etiqueta, type PapelEtiqueta } from "@/components/ui/Etiqueta";
import type { Farol as TipoFarol } from "@/lib/api/cliente";

/** Farol nunca só por cor: sempre ícone e texto (acessibilidade). Visual de lozenge semântico do ADS. */
const APARENCIA: Record<TipoFarol, { icone: string; texto: string; papel: PapelEtiqueta }> = {
  verde: { icone: "✔", texto: "No alvo", papel: "sucesso" },
  amarelo: { icone: "!", texto: "Atenção", papel: "alerta" },
  vermelho: { icone: "✖", texto: "Fora do alvo", papel: "perigo" },
  sem_dado: { icone: "–", texto: "Sem dado", papel: "neutro" },
};

export function textoFarol(farol: TipoFarol): string {
  return APARENCIA[farol].texto;
}

export function Farol({ farol }: { farol: TipoFarol }) {
  const { icone, texto, papel } = APARENCIA[farol];
  return (
    <Etiqueta papel={papel} icone={icone} data-farol={farol}>
      {texto}
    </Etiqueta>
  );
}

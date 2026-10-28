const NUMERO = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 4 });

export function numero(valor: number | null | undefined): string {
  return valor === null || valor === undefined ? "—" : NUMERO.format(valor);
}

/** "2026-10" → "10/2026" */
export function periodo(texto: string): string {
  const [ano, mes] = texto.split("-");
  return `${mes}/${ano}`;
}

/** Aceita "1.234,5" (pt-BR) ou "1234.5"; devolve null se não for número. */
export function lerNumero(texto: string): number | null {
  const limpo = texto.trim();
  const normalizado = limpo.includes(",") ? limpo.replace(/\./g, "").replace(",", ".") : limpo;
  const valor = Number(normalizado);
  return limpo !== "" && Number.isFinite(valor) ? valor : null;
}

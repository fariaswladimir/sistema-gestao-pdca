import createClient from "openapi-fetch";

import { cabecalhosDaSessao } from "@/lib/sessao";

import type { components, paths } from "./esquema";

export type ErroApi = components["schemas"]["ErroSaida"];
export type IndicadorResumo = components["schemas"]["IndicadorResumo"];
export type Farol = IndicadorResumo["farol"];

/** Cliente tipado da API com o usuário da sessão. Só no servidor (Server Components e Server Actions). */
export async function clienteApi() {
  const headers = await cabecalhosDaSessao();
  if (!headers) return null;
  return createClient<paths>({ baseUrl: process.env.API_URL, headers });
}

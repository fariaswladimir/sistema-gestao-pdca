import createClient from "openapi-fetch";

import { auth } from "@/auth";

import type { components, paths } from "./esquema";

export type ErroApi = components["schemas"]["ErroSaida"];
export type IndicadorResumo = components["schemas"]["IndicadorResumo"];
export type Farol = IndicadorResumo["farol"];

/** Cliente tipado da API com o token da sessão. Só no servidor (Server Components e Server Actions). */
export async function clienteApi() {
  const sessao = await auth();
  if (!sessao?.accessToken || sessao.erro) return null;
  return createClient<paths>({
    baseUrl: process.env.API_URL,
    headers: { Authorization: `Bearer ${sessao.accessToken}` },
  });
}

import { cookies } from "next/headers";

import { auth } from "@/auth";

/** Primeiras versões (AGENTS.md): sem login real; o usuário é escolhido numa lista. `oidc` religa o Keycloak. */
export const modoLocal = () => (process.env.AUTH_MODO ?? "local") === "local";

export const COOKIE_USUARIO_LOCAL = "usuario_local";

/** Cabeçalhos que identificam o usuário para a API, ou `null` sem sessão. Só no servidor. */
export async function cabecalhosDaSessao(): Promise<Record<string, string> | null> {
  if (modoLocal()) {
    const id = (await cookies()).get(COOKIE_USUARIO_LOCAL)?.value;
    return id ? { "X-Usuario-Local": id } : null;
  }
  const sessao = await auth();
  if (!sessao?.accessToken || sessao.erro) return null;
  return { Authorization: `Bearer ${sessao.accessToken}` };
}

/** Destino depois de entrar: só caminhos internos (evita redirecionamento aberto). */
export function destinoSeguro(volta: string | null | undefined) {
  return volta && volta.startsWith("/") && !volta.startsWith("//") ? volta : "/meus-indicadores";
}

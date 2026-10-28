import { signIn } from "@/auth";

/** Vai direto para o login do Keycloak e volta para `?volta=` (só caminhos internos). */
export async function GET(request: Request) {
  const volta = new URL(request.url).searchParams.get("volta") ?? "";
  const destino = volta.startsWith("/") && !volta.startsWith("//") ? volta : "/meus-indicadores";
  await signIn("keycloak", { redirectTo: destino });
}

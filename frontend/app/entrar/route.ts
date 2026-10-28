import { redirect } from "next/navigation";

import { signIn } from "@/auth";
import { destinoSeguro, modoLocal } from "@/lib/sessao";

/** Modo local: vai para a escolha de usuário. Modo oidc: vai direto para o login do Keycloak. */
export async function GET(request: Request) {
  const destino = destinoSeguro(new URL(request.url).searchParams.get("volta"));
  if (modoLocal()) redirect(`/escolher-usuario?volta=${encodeURIComponent(destino)}`);
  await signIn("keycloak", { redirectTo: destino });
}

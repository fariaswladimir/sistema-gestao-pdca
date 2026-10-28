"use server";

import { getToken } from "next-auth/jwt";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

import { signOut } from "@/auth";

/** Encerra a sessão da web e a do Keycloak (senão o próximo login entraria sem pedir senha). */
export async function sair() {
  const token = await getToken({
    req: { headers: await headers() },
    secret: process.env.AUTH_SECRET,
    secureCookie: process.env.AUTH_URL?.startsWith("https://") ?? false,
  });
  await signOut({ redirect: false });
  const destino = new URL(`${process.env.AUTH_KEYCLOAK_ISSUER}/protocol/openid-connect/logout`);
  destino.searchParams.set("client_id", process.env.AUTH_KEYCLOAK_ID ?? "");
  destino.searchParams.set("post_logout_redirect_uri", `${process.env.AUTH_URL}/`);
  if (token?.idToken) destino.searchParams.set("id_token_hint", token.idToken);
  redirect(destino.toString());
}

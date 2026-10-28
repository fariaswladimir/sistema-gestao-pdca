"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { COOKIE_USUARIO_LOCAL, destinoSeguro, modoLocal } from "@/lib/sessao";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/** Modo local: guarda o colaborador escolhido (a API confere se existe e está ativo). */
export async function escolherUsuario(dados: FormData) {
  const id = String(dados.get("id") ?? "");
  if (!modoLocal() || !UUID.test(id)) redirect("/entrar");
  (await cookies()).set(COOKIE_USUARIO_LOCAL, id, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    secure: process.env.AUTH_URL?.startsWith("https://") ?? false,
  });
  redirect(destinoSeguro(String(dados.get("volta") ?? "")));
}

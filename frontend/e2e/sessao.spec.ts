import { expect, test } from "@playwright/test";

import { entrar, MODO_OIDC } from "./apoio";

test.skip(MODO_OIDC, "escolha de usuário só existe no modo local");

test("sem usuário escolhido, a página leva à escolha de usuário", async ({ page }) => {
  await page.goto("/meus-indicadores");
  await expect(page).toHaveURL(/\/escolher-usuario\?volta=%2Fmeus-indicadores/);
  await expect(page.getByRole("heading", { name: "Entrar" })).toBeVisible();
});

test("após escolher, mostra os indicadores com o nome do usuário; sair volta à escolha", async ({ page }) => {
  await entrar(page, "ana");
  await expect(page.getByRole("heading", { name: "Meus indicadores" })).toBeVisible();
  await expect(page.getByText("Olá, Ana.")).toBeVisible();

  await page.getByRole("button", { name: "Sair" }).click();
  await expect(page).toHaveURL(/\/escolher-usuario$/);
  await page.goto("/meus-indicadores");
  await expect(page).toHaveURL(/\/escolher-usuario/);
});

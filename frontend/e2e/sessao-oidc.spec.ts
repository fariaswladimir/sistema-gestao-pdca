import { expect, test } from "@playwright/test";

import { entrar, MODO_OIDC } from "./apoio";

// Login real (Keycloak), religado na fatia de autenticação. Roda só com AUTH_MODO=oidc no compose
// (perfil `oidc`) e E2E_AUTH=oidc no Playwright.
test.skip(!MODO_OIDC, "modo oidc desligado nas primeiras versões");

test("sem login, a página leva ao login do Keycloak", async ({ page }) => {
  await page.goto("/meus-indicadores");
  await expect(page).toHaveURL(/keycloak\.localhost:8080\/realms\/gestao\/protocol\/openid-connect\/auth/);
});

test("após entrar, mostra os indicadores com o nome do usuário; sair encerra a sessão", async ({ page }) => {
  await entrar(page, "ana");
  await expect(page.getByRole("heading", { name: "Meus indicadores" })).toBeVisible();
  await expect(page.getByText("Olá, Ana.")).toBeVisible();

  await page.getByRole("button", { name: "Sair" }).click();
  await expect(page.locator("#username")).toBeVisible(); // de volta ao login, sem confirmação
  await page.goto("/meus-indicadores");
  await expect(page.locator("#username")).toBeVisible(); // a sessão do Keycloak também acabou
});

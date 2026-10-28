import { expect, type Page } from "@playwright/test";

/** Modo da bateria: `local` (padrão das primeiras versões) ou `oidc` (E2E_AUTH=oidc, Keycloak no compose). */
export const MODO_OIDC = process.env.E2E_AUTH === "oidc";

const SENHA_DEV = "senha-dev-123";

/** Entra como o colaborador: escolhendo na lista (local) ou pela tela do Keycloak (oidc). */
export async function entrar(page: Page, usuario: string) {
  await page.goto("/");
  if (MODO_OIDC) {
    await expect(page).toHaveURL(/keycloak\.localhost:8080/);
    await page.locator("#username").fill(usuario);
    await page.locator("#password").fill(SENHA_DEV);
    await page.locator("#kc-login").click();
  } else {
    await expect(page).toHaveURL(/\/escolher-usuario/);
    await page.getByRole("button", { name: new RegExp(`^${usuario}\\b`, "i") }).click();
  }
  await expect(page).toHaveURL(/\/meus-indicadores$/);
}

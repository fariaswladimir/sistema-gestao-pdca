import { expect, type Page } from "@playwright/test";

export const SENHA_DEV = "senha-dev-123";

/** Login pela tela do Keycloak (usuários do realm de desenvolvimento). */
export async function entrar(page: Page, usuario: string) {
  await page.goto("/");
  await expect(page).toHaveURL(/keycloak\.localhost:8080/);
  await page.locator("#username").fill(usuario);
  await page.locator("#password").fill(SENHA_DEV);
  await page.locator("#kc-login").click();
  await expect(page).toHaveURL(/\/meus-indicadores$/);
}

import { expect, type Page, test } from "@playwright/test";

import { entrar } from "./apoio";

function cartao(page: Page, codigo: string) {
  return page.getByRole("article", { name: new RegExp(codigo) });
}

test("lançar o valor do mês mostra o farol na hora; relançar exige justificativa", async ({ page }) => {
  await entrar(page, "ana");
  const ind01 = cartao(page, "IND-01");
  await expect(ind01.locator("[data-farol]")).toHaveText(/Sem dado/);
  await expect(ind01.getByLabel("Justificativa da correção")).toHaveCount(0);

  // Lança 85 (meta 80): verde, sem recarregar a página.
  await ind01.getByLabel("Valor").fill("85");
  await ind01.getByRole("button", { name: "Lançar" }).click();
  await expect(ind01.locator("[data-farol]")).toHaveText(/No alvo/);
  await expect(ind01.locator("[data-farol]")).toHaveAttribute("data-farol", "verde");
  await expect(ind01.getByTestId("valor-atual")).toHaveText("85 %");

  // Relançar sem justificativa: a API recusa e a tela explica.
  await ind01.getByLabel("Valor").fill("70,5");
  await ind01.getByRole("button", { name: "Lançar" }).click();
  await expect(ind01.getByRole("alert")).toContainText("justificativa");
  await expect(ind01.locator("[data-farol]")).toHaveText(/No alvo/);

  // Com justificativa: substitui o valor e o farol passa a vermelho.
  await ind01.getByLabel("Justificativa da correção").fill("erro de digitação");
  await ind01.getByRole("button", { name: "Lançar" }).click();
  await expect(ind01.locator("[data-farol]")).toHaveText(/Fora do alvo/);
  await expect(ind01.getByTestId("valor-atual")).toHaveText("70,5 %");
});

test("cada colaborador vê só os próprios indicadores", async ({ page }) => {
  await entrar(page, "ana");
  await expect(cartao(page, "IND-01")).toBeVisible();
  await expect(cartao(page, "IND-02")).toHaveCount(0);
});

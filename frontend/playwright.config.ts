import { defineConfig, devices } from "@playwright/test";

/** E2E contra o ambiente do compose (web, api, keycloak e banco com seed). */
export default defineConfig({
  testDir: "./e2e",
  globalSetup: "./e2e/preparar.ts",
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : "list",
  use: {
    baseURL: process.env.E2E_BASE_URL ?? "http://localhost:3000",
    locale: "pt-BR",
    trace: "retain-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});

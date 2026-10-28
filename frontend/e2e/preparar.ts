import { execSync } from "node:child_process";
import path from "node:path";

/**
 * Zera medições, auditoria e fila do banco do compose antes da bateria E2E.
 * Só para ambiente local/CI: defina E2E_SEM_RESET=1 para rodar contra outro ambiente.
 */
export default function preparar() {
  if (process.env.E2E_SEM_RESET) return;
  const sql = "truncate medicao, evento_auditoria, fila_tarefa";
  execSync(`docker compose exec -T db psql -U gestao -d gestao -c "${sql}"`, {
    cwd: path.resolve(import.meta.dirname, "../.."),
    stdio: "inherit",
  });
}

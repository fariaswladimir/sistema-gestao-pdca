---
name: regra-motor
description: Use ao criar regras do motor (farol, consolidação, abertura automática, prazos, diagnóstico).
---

# Regra do motor

- Regras puras em `backend/app/motor/` recebem dados e devolvem decisão; não acessam banco.
- Disparo por evento de domínio (`MedicaoRegistrada`, `AcaoVenceu`, `PeriodoFechado`) no worker.
- Toda regra é idempotente: rodar duas vezes não duplica efeitos (ex.: não abre segunda anomalia no mesmo período).
- Teste unitário com tabela de casos (parametrize) cobrindo as três polaridades e `sem_dado`.

---
description: Gerar plan.md e tasks.md de uma fatia com spec aprovada.
---

1. Confirme que `specs/Fxx-*/spec.md` está com status Aprovada. Se não, pare e sugira /nova-fatia.
2. Leia a spec, o `acceptance.feature`, os documentos transversais em `specs/_*.md` e as `decisoes.md` das fatias anteriores.
3. Revise o `plan.md` existente (ou crie a partir de @specs/_templates/plan.md) cobrindo:
   modelo de dados (tabelas e migrações), regras de domínio, eventos, endpoints (método, rota, permissão),
   ferramentas MCP (se houver), telas e componentes, testes por camada, riscos.
4. Revise o `tasks.md`: tarefas de 30 min a 2 h, em ordem, cada uma com "Pronto quando" verificável.
   A primeira tarefa é sempre o teste de aceitação falhando (vermelho).
5. Apresente o plano como artefato de Implementation Plan e PARE para revisão do humano.

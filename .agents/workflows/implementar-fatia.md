---
description: Implementar as tarefas de uma fatia em ordem, com testes primeiro.
---

1. Confirme spec Aprovada e plan.md revisado. Crie/entre na branch `fatia/Fxx-nome`.
2. Leia `tasks.md` e escolha a primeira tarefa não marcada.
3. Para cada tarefa:
   a. Escreva ou ative o teste que prova a tarefa (deve falhar).
   b. Implemente o mínimo para passar, seguindo @.agents/rules/20-stack-convencoes.md.
   c. Rode `make test` e o teste específico. Para rotas ou ferramentas MCP novas, rode `make test-perms`.
   d. Marque a tarefa como feita em `tasks.md` e faça commit `Fxx: <tarefa>`.
4. Se a tarefa exigir algo fora da spec, PARE e descreva a divergência; não improvise regra de negócio.
5. Ao concluir todas as tarefas, chame /verificar-fatia.

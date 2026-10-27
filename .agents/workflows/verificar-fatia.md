---
description: Verificar se a fatia atende ao Definition of Done.
---

1. Rode `make check` e `make test-slice F=Fxx`. Registre a saída resumida.
2. Para cada cenário de `acceptance.feature`, confirme que existe teste correspondente e que passou.
3. Rode /revisar-seguranca para os arquivos alterados na branch.
4. Se a fatia tem interface, rode `make e2e` e capture screenshots com o navegador do Antigravity.
5. Se a fatia toca IA, rode `make evals` e compare com a linha de base.
6. Confira o "Pronto quando" da spec. Se algo falhar, volte para /implementar-fatia com a lista de pendências.
7. Gere um Walkthrough com: o que foi entregue, evidências (testes, screenshots), decisões, pendências.

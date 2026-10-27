# F00 – Tarefas

- [ ] T1 Estrutura do repositório (backend, frontend, Makefile, docker-compose). Pronto quando: `make up` sobe tudo e `/saude` responde.
- [ ] T2 Testes de aceitação da F00 rodando e falhando. Pronto quando: `make test-slice F=F00` executa e falha nos passos.
- [ ] T3 Migração inicial e seed. Pronto quando: `make migrate && make seed` cria as tabelas e os dados.
- [ ] T4 Autenticação OIDC com Keycloak local e rota `/eu`. Pronto quando: cenário "acesso sem login" passa.
- [ ] T5 `calcular_farol` com testes unitários das 3 polaridades (só maior_melhor exposto). Pronto quando: unitários verdes.
- [ ] T6 Rotas de indicadores e medição com permissão e escopo. Pronto quando: cenários de farol e 404 passam.
- [ ] T7 Auditoria de medição e regra de justificativa. Pronto quando: cenário de relançamento passa.
- [ ] T8 Tela "Meus indicadores" com lançamento. Pronto quando: `make e2e` passa.
- [ ] T9 Pipeline de CI e deploy em homologação. Pronto quando: merge na principal publica em homologação.
- [ ] T10 Matriz de permissões inicial e `make test-perms`. Pronto quando: testes gerados passam.

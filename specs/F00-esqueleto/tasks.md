# F00 – Tarefas

Branch: `fatia/F00-esqueleto`. Cada tarefa termina com testes verdes do que ela toca e um commit `F00: ...`.

- [x] T1 Aceitação vermelha. `backend/pyproject.toml` (dependências e ferramentas), app FastAPI vazio, `conftest` com banco de teste,
      `tests/acceptance/F00/` lendo `specs/F00-esqueleto/acceptance.feature` e passos escritos.
      Pronto quando: `make test-slice F=F00` coleta todos os cenários e **todos falham** nas asserções (nenhum erro de coleta).
- [x] T2 Infra local. Dockerfiles, compose com healthchecks, Keycloak 26 com realm exportado, `.env.example` completo,
      correções do `Makefile`, `GET /saude` com versão e checagem do banco.
      Pronto quando: `make up` sobe db, keycloak, api, worker e web; `curl localhost:8000/saude` dá 200; cenário "saúde" verde.
- [x] T3 Modelos e migração inicial. Tabelas e extensões do plano, UUID v7, `NUMERIC`.
      Pronto quando: `make migrate` cria tudo; teste de integração sobe e desce a migração (`downgrade base`) sem erro.
- [x] T4 Seed idempotente e usuários do realm de dev.
      Pronto quando: `make seed` duas vezes seguidas não duplica nada; ana e bruno entram no Keycloak local.
- [x] T5 Motor do farol. `calcular_farol` com as 3 polaridades e `Decimal`; meta vigente do período.
      Pronto quando: unitários verdes, incluindo os limites 80/76/75,9 e `sem_dado`.
- [x] T6 Autenticação na API. Validação do JWT via JWKS, `usuario_atual`, vínculo `sub_oidc`/e-mail, `GET /eu`, handler de erros.
      Pronto quando: unitários de token verdes; cenário "acesso sem login" verde.
- [ ] T7 Permissões. `permissoes.py` espelhando a matriz, `exigir_permissao`, `escopo_indicadores`, teste de paridade com `matriz.yaml`.
      Pronto quando: teste de paridade verde e `exigir_permissao` coberta por unitários.
- [ ] T8 Leitura de indicadores. `GET /indicadores/meus` e `GET /indicadores/{id}` com relógio injetável.
      Pronto quando: cenários "vê seu indicador sem dado" e "não vê indicador de outro responsável" verdes.
- [ ] T9 Lançamento de medição. `PUT /indicadores/{id}/medicoes/{periodo}`, farol gravado, regra de justificativa,
      auditoria na mesma transação e `MedicaoRegistrada` no outbox.
      Pronto quando: os 5 exemplos de farol e o cenário de relançamento (422 + auditoria 70 → 82) verdes; `make test-slice F=F00` todo verde.
- [ ] T10 Worker da fila. Laço com `SKIP LOCKED` e registro de handlers.
      Pronto quando: teste de integração mostra `MedicaoRegistrada` saindo de `pendente` para `concluida`.
- [ ] T11 Matriz executável. Gerador a partir de `matriz.yaml` e do registro rota → ação.
      Pronto quando: `make test-perms` verde para os 7 perfis × 2 ações × (próprio, de outro responsável).
- [ ] T12 Contrato da API. Schemathesis sobre `/openapi.json`.
      Pronto quando: `make test-contract` verde.
- [ ] T13 Web: base e login. Next.js + Tailwind, Auth.js com Keycloak, cliente gerado do OpenAPI, lint e typecheck.
      Pronto quando: no navegador, `/` sem sessão vai ao login do Keycloak e, após entrar como ana, mostra `/meus-indicadores` com o nome dela.
- [ ] T14 Web: Meus indicadores. Componente `Farol` (cor + ícone + texto), cartões e `LancarMedicao`.
      Pronto quando: `make e2e` verde (login → lançar → ver farol; relançar sem justificativa → erro; sem login → login).
- [ ] T15 CI. Jobs `check`, `e2e` (com compose) e `publicar` (imagens no GHCR).
      Pronto quando: um PR mostra `check` e `e2e` verdes; um push na `main` publica as imagens com o SHA como tag.
- [ ] T16 Homologação. `docker-compose.homolog.yml` (Keycloak em modo produção, Caddy HTTPS, Uptime Kuma),
      runner self-hosted e job `deploy-homologacao` com migração e checagem de `/saude`.
      Pronto quando: um merge na `main` aparece em homologação com a nova versão em `/saude` e o Uptime Kuma alerta quando a API para.

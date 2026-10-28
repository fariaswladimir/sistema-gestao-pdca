# F00-esqueleto – Decisões

| Data | Decisão | Motivo |
| --- | --- | --- |
| 2026-10-27 | Login na v1 com usuário e senha próprios do sistema, sem SSO corporativo. | Decisão do dono do produto na aprovação da F00. |
| 2026-10-27 | Keycloak como provedor de identidade também em homologação e produção, com usuários locais. | Mantém OIDC do plano; Keycloak já entrega hash de senha, redefinição e bloqueio por força bruta; federar com Entra ID depois não muda o código. |
| 2026-10-27 | Homologação e produção em servidor interno com Docker Compose. | Decisão do dono do produto na aprovação da F00. |
| 2026-10-27 | Tolerância padrão de 5% da meta confirmada. | Decisão do dono do produto na aprovação da F00. |
| 2026-10-27 | T3 executada antes da T2. | O `Contexto` do Gherkin cria dados em todos os cenários, inclusive no de saúde; sem tabelas nenhum cenário fica verde. |
| 2026-10-27 | Enums gravados como texto com CHECK, sem tipo nativo do Postgres. | Acrescentar valor (ex.: `importacao` na F10) vira troca de CHECK, sem `ALTER TYPE`. |
| 2026-10-27 | `pytest.ini` e `conftest.py` na raiz, fixtures no plugin `backend/apoio_testes/fixtures.py`. | Um único rootdir para `backend/tests` e `tests/`; pytest-bdd lê a feature direto de `specs/`. |
| 2026-10-27 | Dados de teste montados por SQL direto (`apoio_testes/dados.py`), não pelo código da aplicação. | Aceitação continua caixa-preta: um bug no serviço não contamina o arranjo do teste. |
| 2026-10-28 | Keycloak atende como `keycloak.localhost:8080` (apelido de rede no compose). | Navegadores resolvem `*.localhost` para 127.0.0.1 e o DNS do Docker resolve o apelido: emissor único para navegador, web e API, sem editar o arquivo hosts. |
| 2026-10-28 | T2 validada com db, keycloak e api; `worker` e `web` sobem a partir da T10 e da T13. | O código desses serviços é dessas tarefas; o compose já os declara. |
| 2026-10-28 | Makefile chama ferramentas via `$(PYTHON) -m` e roda o pytest a partir da raiz. | Funciona com venv ativo, com `PYTHON=` explícito no Windows e no CI. |

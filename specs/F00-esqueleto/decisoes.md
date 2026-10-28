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
| 2026-10-28 | `menor_melhor` e `faixa` no motor seguem a RN3 da spec F01 (ainda em rascunho); só `maior_melhor` é aceita pelo serviço na F00. | Plano aprovado pede as três polaridades testadas no motor. Se a F01 mudar a regra na aprovação, ajustar `motor/farol.py` e a tabela de casos. |
| 2026-10-28 | Indicador sem meta vigente fica `sem_dado`. | A spec não trata o caso; o seed sempre tem meta. Reavaliar na F01 (cadastro de metas). |
| 2026-10-28 | E-mail já vinculado a outro `sub` não é revinculado (403). | Evita sequestro de conta se alguém criar no Keycloak outro usuário com o mesmo e-mail. |
| 2026-10-28 | O cenário "acesso sem login" fecha na T8, junto com a rota `/indicadores/meus`; na T6 o 401 é provado em `/eu`. | A rota do cenário pertence à T8. |
| 2026-10-28 | Auditoria grava valores como texto decimal (`"70.0000"`); a API devolve número. | Trilha exata, sem erro de ponto flutuante; cliente recebe JSON numérico. |
| 2026-10-28 | Lançamento simultâneo no mesmo período responde 409. | A unicidade (indicador, período) no banco é a última barreira; o cliente recarrega e relança com justificativa. |
| 2026-10-28 | A matriz de testes descobre as rotas pela ação marcada em `exigir_permissao`, em vez de um registro manual rota → ação. | Rota nova entra sozinha na matriz; sem exemplo de requisição, o teste falha e obriga a cobrir. |
| 2026-10-28 | FastAPI 0.162: routers incluídos são `_IncludedRouter` e `ModelField` não tem `type_`; o gerador desce por `original_router` e lê `field_info.annotation`. | Mudança de API interna do FastAPI; se quebrar de novo numa atualização, o `test_ha_rotas_protegidas` acusa. |
| 2026-10-28 | Envelope único de erro `{detalhe, erros?}` para erros de domínio, de validação (422) e do framework (400, 405), documentado no OpenAPI. | O Schemathesis apontou 401/403/400 não documentados e dois formatos de 422; o cliente da web passa a tratar um formato só. |
| 2026-10-28 | `periodo` validado no contrato (`^[1-9]\d{3}-(0[1-9]\|1[0-2])$`). | Ano 0000 passava pelo formato e quebrava em `date(0, ...)` (seria 500). |
| 2026-10-28 | `valor` documentado como número entre ±99.999.999.999.999 e arredondado para 4 casas (meio para cima). | Cabe em `NUMERIC(18,4)`; o `Decimal` do Pydantic aparecia no contrato como "número ou texto". |
| 2026-10-28 | Ruff com `line-length 110` em `backend/`, `tests/` e `conftest.py`; migrações geradas ficam fora do lint. | Migrações são imutáveis; reformatar uma já aplicada violaria a regra 8. |

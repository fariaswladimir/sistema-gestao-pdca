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
| 2026-10-28 | Web: Next.js 16.4, React 19, Tailwind 4, Auth.js `5.0.0-beta.32` (versões fixas), TypeScript 5.9 e ESLint 9. | Auth.js 5 ainda é beta, mas declara suporte ao Next 16; TypeScript 7 (reescrita em Go) ficou de fora por risco com ferramentas. |
| 2026-10-28 | Chamadas à API só no servidor (Server Components e Server Actions); `id_token` fica só no cookie criptografado, fora da sessão. | O access token aparece em `/api/auth/session` (padrão do Auth.js, vida de 5 min); o `id_token` serve só ao logout. TODO: avaliar tirar o access token da sessão. |
| 2026-10-28 | Logout encerra a sessão do Keycloak com `id_token_hint`. | Sem ele, o Keycloak pede confirmação e o próximo login entraria sem senha. |
| 2026-10-28 | `npm run dev` direto no Windows exige `127.0.0.1 keycloak.localhost` no arquivo hosts; no Docker e no Playwright funciona sem isso. | O Node no Windows não resolve `*.localhost`; navegadores e o DNS do Docker resolvem. |
| 2026-10-28 | O campo de justificativa aparece quando o período atual já tem valor ou quando a API responde `justificativa_obrigatoria`; a regra continua só na API. | A tela não duplica a RN3; para períodos passados ela aprende com a resposta. |
| 2026-10-28 | O E2E zera `medicao`, `evento_auditoria` e `fila_tarefa` do compose antes de rodar (`E2E_SEM_RESET=1` desliga). | Bateria repetível; nunca apontar o E2E para homologação ou produção sem essa variável. |
| 2026-10-28 | Versões Python fixadas em `backend/restricoes.txt` (freeze do venv testado), usadas no CI e na imagem. | pytest 9.2.0 saiu no meio da fatia e quebrou o pytest-bdd 9.0.0 só no CI. Atualizar = regenerar e rodar a suíte. |
| 2026-10-28 | Worker sobrevive a banco indisponível ou sem migração (registra e tenta de novo); serviços com `restart: unless-stopped`. | No primeiro `up` o worker sobe antes da migração e morria. Vale para homologação também. |
| 2026-10-28 | Healthcheck do worker por arquivo de batimento (< 60 s). | O Compose do runner novo (Ubuntu 26) recusa no `--wait` serviço sem healthcheck; de quebra, worker travado vira `unhealthy`. |
| 2026-10-28 | Em falha do E2E, o CI publica `compose up`, `ps` e logs como anotação. | Anotações são legíveis pela API sem login; os logs completos exigem token. |
| 2026-10-28 | T15 fechada com `check` e `e2e` verdes no GitHub (run 40657255562); `publicar` (GHCR) só roda em push na `main` e será confirmado no merge. | |
| 2026-10-28 | `docker-compose.homolog.yml` é um arquivo próprio, não sobreposição do de dev (desvio do plan). | O de dev publica a porta do banco, compila imagens e roda o Keycloak em modo dev; desfazer isso por sobreposição seria frágil. |
| 2026-10-28 | Homologação com um só nome: `/` web, `/auth` Keycloak, `:3443` Uptime Kuma, todos atrás do Caddy; só ele publica portas. | Um certificado, um registro de DNS; dentro do compose o nome aponta para o Caddy (mesmo truque do dev), então o emissor é igual para navegador, web e API. |
| 2026-10-28 | TLS por variável: CA interna do Caddy (padrão) ou certificado da organização; a web confia na raiz via `NODE_EXTRA_CA_CERTS`. | Permite subir sem esperar a TI; o healthcheck do Caddy publica só a raiz pública num volume legível pela web (as chaves continuam em `/data`, só do Caddy). |
| 2026-10-28 | Realm de homologação separado, com marcadores `${...}`; usuários de demonstração entram com senha inicial e `requiredActions: UPDATE_PASSWORD`. | Sem senhas no repositório; na importação o Keycloak ignora `temporary` da credencial, só a ação requerida força a troca. |
| 2026-10-28 | `deploy-homologacao` só roda com a variável `HOMOLOG_ATIVA=true` e runner com rótulo `homologacao`; o mesmo `infra/homolog/implantar.sh` serve ao job e à operação manual. | Sem a variável o job ficaria na fila esperando um runner inexistente. |
| 2026-10-28 | Monitores do Uptime Kuma configurados à mão (roteiro no README). | A versão 1.x não tem configuração declarativa nem API REST. |
| 2026-10-28 | Realm de dev com ids fixos de usuário. | Recriar o contêiner do Keycloak (H2 do modo dev) gerava outro `sub`; a API, corretamente, recusava revincular o e-mail e o ambiente local quebrava. |

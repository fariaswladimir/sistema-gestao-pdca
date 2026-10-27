# F00 – Plano

Spec: Aprovada em 2026-10-27. Decisões de produto em `decisoes.md`.

## Arquitetura de autenticação
- **Keycloak** é o provedor de identidade em todos os ambientes (realm `gestao`), com usuários de login e senha
  próprios. Política do realm: senha com no mínimo 10 caracteres, detecção de força bruta ligada, auto-cadastro desligado.
- **Web (Next.js)** faz o login OIDC (Authorization Code + PKCE) com Auth.js (`next-auth` v5, provedor Keycloak).
  As "rotas de sessão" da spec são as do Auth.js na web: `/api/auth/signin`, `/api/auth/callback/keycloak`, `/api/auth/signout`.
- **API (FastAPI)** é stateless: valida o `Authorization: Bearer <access_token>` (JWT RS256) contra o JWKS do Keycloak,
  conferindo `iss`, `aud` (`gestao-api`), `exp`. Sem token ou com token inválido: 401.
  É o mesmo mecanismo que F06 (API pública) e F07 (MCP com token do usuário) vão reusar.
- **Perfil e setor vêm do banco** (`colaborador.perfil`, `colaborador.setor_id`), nunca de papéis do Keycloak.
  Vínculo token → colaborador por `sub_oidc`; no primeiro acesso, por e-mail verificado, gravando o `sub_oidc`.
  Token válido sem colaborador ativo: 403.
- Emissor público × rede interna do Docker: `OIDC_ISSUER` (URL vista pelo navegador, valida `iss`)
  e `OIDC_JWKS_URL` (URL interna para buscar as chaves). JWKS em cache com renovação quando surge `kid` desconhecido.

## Modelo de dados e migrações
Uma migração `F00 esqueleto` (Alembic, com `downgrade`):
- Extensões `ltree` e `vector` (`CREATE EXTENSION IF NOT EXISTS`); criadas agora, usadas a partir da F01/F09.
- `setor`: nome, sigla, setor_pai_id (FK, null), ativo.
- `colaborador`: nome, email (único), setor_id, perfil (enum dos 7 perfis), status (ativo, afastado, desligado), sub_oidc (único, null).
- `ciclo`: nome, inicio, fim, status. Mínimo necessário para achar a meta vigente de um período (ver decisões).
- `tipo_indicador`: nome, nivel, natureza, polaridade, consolidacao, origem (enums completos do modelo canônico).
- `indicador`: codigo (único), nome, tipo_id, setor_id, responsavel_id, unidade, periodicidade, tolerancia_pct (default 5), ativo.
- `meta`: indicador_id, ciclo_id, periodo (null = meta do ciclo), valor, valor_min, valor_max.
- `medicao`: indicador_id, periodo (date, dia 1), valor, origem, registrado_por, farol, justificativa_correcao;
  único (indicador_id, periodo).
- `evento_auditoria`: entidade, entidade_id, acao, antes (jsonb), depois (jsonb), ator_id, ator_tipo, modelo_ia, canal, em.
- `fila_tarefa`: tipo, payload (jsonb), status (pendente, em_execucao, concluida, falhou), tentativas, executar_em.
- Todas com `id` UUID v7 (gerado na aplicação, pacote `uuid6`), `criado_em`, `atualizado_em`. FKs com `ondelete` explícito.
- Valores numéricos em `NUMERIC(18,4)`, `Decimal` no Python. Nada de float no cálculo do farol.
- `indicador.caminho`, `pai_id`, `objetivo_id`, `peso`, `publicado` ficam para a F01/F02 (`# TODO(F01)`).

Seed (`python -m app.seed`, idempotente): setores Sede > Piloto/Outro; colaboradores `ana` (Piloto) e `bruno` (Outro)
como colaborador, mais um usuário por perfil para os testes de permissão; um ciclo 2026; tipo `maior_melhor`;
`IND-01` (resp. ana) e `IND-02` (resp. bruno) com meta 80 e tolerância 5%. Os mesmos usuários estão no realm de dev
exportado em `infra/keycloak/realm-gestao.json`, com senhas só de desenvolvimento.

## Regras de domínio e motor
- `motor/farol.py`: `calcular_farol(valor: Decimal | None, meta: Meta, polaridade, tolerancia_pct) -> Farol`, função pura.
  Implementa as três polaridades com testes unitários, mas o serviço só aceita `maior_melhor` nesta fatia (RN4).
  Limite do amarelo inclusivo: `valor >= meta * (1 - tol)`.
- Meta vigente do período: a meta com `periodo` igual; senão a meta do ciclo que contém o período.
- `dominio/medicoes.py`: regra de relançamento (RN3). Já existe medição no período e não veio justificativa: `JustificativaObrigatoria` (422).
- `dominio/periodo.py`: converte `"2026-10"` para `date(2026, 10, 1)`; "período atual" vem de um `Relogio`
  injetável (fuso `America/Recife`), congelado nos testes.
- `seguranca/permissoes.py`: mapa perfil → ações completo, espelhando `_perfis-permissoes.md`; `exigir_permissao(acao)`;
  `escopo_indicadores(usuario)`, que nesta fatia filtra por `responsavel_id = usuario.id` (RN2). `# TODO(F01)`: escopo por setor.
- `auditoria.py`: `registrar_auditoria(entidade, id, acao, antes, depois, ator, canal)`, na mesma transação da escrita (RN5).
- `dominio/erros.py` + um handler único: `NaoEncontrado` → 404, `JustificativaObrigatoria` → 422, `SemPermissao` → 403.

## Eventos
- `MedicaoRegistrada(indicador_id, periodo, valor, farol, farol_anterior)` é publicado em `motor/eventos.py`
  por *outbox*: grava em `fila_tarefa` na mesma transação da medição.
- `motor/worker.py`: laço que pega tarefas com `FOR UPDATE SKIP LOCKED`, despacha para handlers registrados e marca
  `concluida`. Ainda não há handlers; tipo sem handler é concluído com log. `# TODO(F03)`: regra de abrir anomalia.

## API (método · rota · permissão)
| Método | Rota | Permissão | Respostas |
| --- | --- | --- | --- |
| GET | /saude | pública | 200 `{status, versao, banco}`; 503 se o banco cair |
| GET | /eu | autenticado | 200 colaborador e perfil; 401; 403 sem cadastro |
| GET | /indicadores/meus | indicador:ler | 200 lista com meta, último valor e farol do período atual |
| GET | /indicadores/{id} | indicador:ler + escopo | 200; 404 fora do escopo ou inexistente |
| PUT | /indicadores/{id}/medicoes/{periodo} | medicao:registrar + escopo | 200 (substituiu), 201 (criou), 403, 404, 422 |

- Corpo do PUT: `{valor: decimal, justificativa?: string}`. Período no formato `AAAA-MM`.
- Ordem de checagem: autenticação (401) → permissão do perfil (403) → escopo (404) → regra (422).
- Logs JSON estruturados (`structlog`), com `request_id`; nunca e-mail nem token em log.
- `versao` vem de `APP_VERSION` (SHA do commit, gravado no build da imagem).

## MCP
Nenhum nesta fatia.

## Telas e componentes
- `/` sem sessão: redireciona para o login do Keycloak (tela padrão do Keycloak com o nome do sistema).
- `/meus-indicadores` (Server Component): um cartão por indicador com nome, meta, último valor e farol do período atual.
- `components/dominio/Farol.tsx`: cor + ícone + texto (`verde ✔ No alvo`, `amarelo ! Atenção`, `vermelho ✖ Fora do alvo`,
  `sem_dado – Sem dado`).
- `LancarMedicao.tsx` (Client Component): período (padrão: atual), valor e justificativa. O campo de justificativa
  aparece e passa a ser obrigatório quando já existe valor no período. Ao salvar, o farol é atualizado sem recarregar.
- Cliente da API gerado do OpenAPI (`openapi-typescript` + `openapi-fetch`) em `frontend/lib/api/`, com o access token da sessão.
- Botão "Sair" (logout no Auth.js e no Keycloak).

## Infra
- `backend/Dockerfile` e `frontend/Dockerfile` multi-stage; `APP_VERSION` como build arg.
- `docker-compose.yml` (dev): healthchecks; Keycloak 26 em `start-dev --import-realm`; `KC_HOSTNAME=http://localhost:8080`.
- `docker-compose.homolog.yml` (sobreposição): Keycloak em modo `start` com banco próprio no mesmo Postgres;
  proxy reverso Caddy com HTTPS; imagens vindas do GHCR; Uptime Kuma checando `/saude` e a web, com alerta por e-mail.
  Erros: logs JSON das aplicações (nível `error`) consultáveis no servidor; alerta quando `/saude` falha.
- CI (GitHub Actions): job `check` (lint, typecheck, testes, matriz, contrato, aceitação); job `e2e` sobe o compose
  e roda o Playwright; job `publicar` constrói e envia as imagens ao GHCR (só na `main`); job `deploy-homologacao` roda num
  **runner self-hosted** dentro do servidor interno: `docker compose pull && up -d && alembic upgrade head`, e confere `/saude`.
- Correções no `Makefile`: alvos `lint`/`typecheck` mudam de diretório errado (`cd frontend` executado dentro de `backend`)
  e engolem a falha do backend por causa do `;`. Passam a usar subshells e `&&`.
- `.env.example`: `OIDC_JWKS_URL`, `OIDC_AUDIENCE`, `AUTH_SECRET`, `AUTH_KEYCLOAK_ID/SECRET/ISSUER`, `APP_VERSION`.

## Testes por camada
- **Unitário** (`backend/tests/unit`): tabela de casos do farol (3 polaridades, limites exatos, `sem_dado`, tolerância 0),
  conversão de período, regra de justificativa, validação de token (expirado, emissor errado, audiência errada, assinatura inválida).
- **Integração** (`backend/tests/integration`): Postgres real; Testcontainers localmente e o serviço `db` no CI
  (via `TEST_DATABASE_URL`). Migração sobe e desce (`upgrade head` → `downgrade base`); unicidade de medição; outbox + worker.
- **Aceitação** (`tests/acceptance/F00/`): pytest-bdd lê **direto** `specs/F00-esqueleto/acceptance.feature`
  (sem cópia, sem link simbólico, que é frágil no Windows). Passos chamam a API real (ASGI + banco de teste).
  Tokens assinados por uma chave RSA de teste, com o JWKS da API apontado para ela; relógio congelado em 2026-10.
- **Permissões** (`tests/permissions/`): gerador lê `matriz.yaml` e um registro `rota → ação`; testa cada perfil
  nas rotas existentes (`indicador:ler`, `medicao:registrar`): permitido → 2xx, negado → 403, outro responsável → 404.
  Ações ainda sem rota ficam fora do gerador (sem `skip`). Um teste garante que `permissoes.py` == `matriz.yaml`.
- **Contrato**: Schemathesis sobre `/openapi.json` com token de colaborador.
- **E2E** (Playwright, Keycloak real do compose): login como ana → lançar 85 → ver "No alvo"; relançar sem justificativa → erro;
  sem login → redireciona para o login.

## Riscos e mitigação
| Risco | Mitigação |
| --- | --- |
| OIDC consumir a fatia (emissor interno × externo, cookies, PKCE) | Realm exportado no repo; `OIDC_ISSUER` separado de `OIDC_JWKS_URL`; testes da API não dependem do Keycloak |
| Servidor interno inacessível a partir do GitHub | Runner self-hosted no servidor puxa as imagens (deploy de dentro para fora) |
| Docker/WSL no Windows (quebras de linha, `make`) | `.gitattributes` com LF (feito); `make` via WSL ou Chocolatey |
| Arredondamento no limite do farol (76 × 75,9) | `Decimal` e `NUMERIC`; casos de limite no unitário e no aceite |
| Escopo provisório (responsável) virar dívida | Escopo isolado em `escopo_indicadores`; `TODO(F01)` e teste que falhará quando F01 trocar a regra |

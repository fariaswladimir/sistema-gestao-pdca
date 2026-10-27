# Sistema de Gestão PDCA e SDCA

Sistema para gerir uma organização pelo método de desdobramento de metas (estilo SGF/FIEPE):
a estratégia vira uma árvore de indicadores; cada nó roda SDCA para manter o resultado e PDCA
para melhorá-lo. A auditoria da gestão (diagnóstico) é calculada a partir dos dados.

## Como trabalhamos
- A unidade de trabalho é a **fatia fina** (F00 a F10), em `specs/`. Cada fatia é vertical:
  atravessa tela, API, serviço, banco e, quando for o caso, integração e IA.
- Ciclo obrigatório: `/nova-fatia` → `/planejar-fatia` → `/implementar-fatia` → `/verificar-fatia` → `/demo-fatia`.
- Nunca implemente sem `spec.md` com status **Aprovada**. Nunca altere uma spec para fazer um teste passar:
  proponha a mudança e pare para o humano aprovar.
- Uma fatia só fecha quando `make check` passa e os cenários de `acceptance.feature` estão verdes.

## Leitura obrigatória antes de qualquer tarefa
- @specs/README.md (processo e status das fatias)
- @specs/_glossario.md
- @specs/_modelo-dados.md
- @specs/_perfis-permissoes.md
- A pasta da fatia em andamento em `specs/Fxx-*/`

## Stack
- Backend: Python 3.12, FastAPI, SQLAlchemy 2 (async), Alembic, Pydantic v2
- Banco: PostgreSQL 16 com extensões `ltree` e `pgvector`
- Frontend: Next.js (React, TypeScript, App Router), Tailwind
- Servidor MCP: SDK oficial `mcp` para Python (transporte Streamable HTTP), montado no mesmo serviço
- Testes: pytest, pytest-bdd (aceitação), Schemathesis (contrato), Playwright (ponta a ponta)
- Infra local: Docker Compose (postgres, keycloak, api, web)

## Comandos
- `make up` sobe o ambiente local; `make down` derruba
- `make migrate` aplica migrações; `make seed` carrega dados de exemplo
- `make test` testes unitários e de integração
- `make test-slice F=F03` testes de aceitação de uma fatia
- `make test-perms` matriz de permissões
- `make test-contract` contrato da API e do MCP
- `make e2e` Playwright
- `make lint` / `make typecheck`
- `make check` tudo acima; é o portão de qualquer entrega

## Estrutura
```
backend/app/        api/ (rotas), dominio/ (regras), servicos/, modelos/, mcp/, ia/, integracoes/, motor/
backend/migrations/ Alembic
frontend/           Next.js
specs/              specs por fatia e documentos transversais
tests/              acceptance/, permissions/, contracts/, evals/
seed/               dados de exemplo anonimizados
```

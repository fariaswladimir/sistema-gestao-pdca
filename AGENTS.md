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

## Diretrizes de versão (decididas pelo dono do produto em 2026-10-28)
Prevalecem sobre specs e regras antigas que digam o contrário; ao tocar numa fatia, alinhe a spec e peça aprovação.
1. **Primeiras versões rodam localmente, sem infraestrutura complexa.** O alvo é `make up` na máquina do
   desenvolvedor. Servidor de homologação, runner self-hosted, HTTPS e monitoramento ficam para quando houver
   servidor (a T16 da F00 está pronta em código e adiada).
2. **Primeiras versões já entregam funcionalidade de verdade**, com:
   - telas usáveis por um usuário real (não só API);
   - dados de exemplo (`make seed`) para abrir e demonstrar;
   - testes automatizados (aceitação verde é o critério de pronto);
   - auditoria das escritas (o ator é o usuário escolhido na sessão local).
3. **Autenticação só a partir da fatia [DECIDIR: F02 ou F03].** Até lá, o modo local (`AUTH_MODO=local`) entra
   escolhendo o usuário numa lista, sem senha e sem Keycloak. O código de login real da F00 (Keycloak/OIDC)
   permanece e é religado por configuração (`AUTH_MODO=oidc`).
4. **Autorização e criação de perfis só nas versões finais (F09/F10).** Até lá, todo usuário vê e altera tudo.
   A matriz de @specs/_perfis-permissoes.md é o alvo futuro; não crie regra de perfil ou escopo nova, e os
   testes de permissão saem do `make check` até lá. Não escreva cenários de 403/404 por perfil nas specs.

## Relatório de situação em HTML (obrigatório em toda resposta ao humano)
A EAP e a etapa da fatia fina são mostradas sempre na página **`docs/eap.html`**, gerada por `make eap`
(`scripts/eap.py`, só biblioteca padrão) a partir de:
- a tabela de fatias de `specs/README.md` (status) e as caixas de `specs/Fxx-*/tasks.md` (percentuais);
- a seção **"Em andamento"** de `specs/README.md`: fatia, etapa (1 spec · 2 plano · 3 implementação ·
  4 verificação · 5 demo), próximos passos (até 3, separados por `|`) e bloqueios ou decisões pendentes do humano.

Ao fim de toda tarefa ou resposta que mude o estado:
1. Atualize as caixas de `tasks.md`, o status na tabela e a seção "Em andamento" (nunca estime de memória).
2. Rode `make eap` (no Windows sem `make`: `python scripts/eap.py`).
3. Termine a resposta com o link para a página e uma linha de resumo, por exemplo:
   `📊 [EAP](docs/eap.html) · F01 etapa 1/5 Spec · geral 15% · bloqueios: 2`.

A página não é versionada (é derivada); quem quiser vê-la roda `make eap` e abre `docs/eap.html` no navegador.

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

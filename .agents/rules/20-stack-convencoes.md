---
trigger: always_on
---

# Stack e convenções

## Backend (Python 3.12, FastAPI)
- Camadas: `api/` (rotas finas, só validação e autorização) → `servicos/` (casos de uso, transação) →
  `dominio/` (regras puras, sem I/O) → `modelos/` (SQLAlchemy). O motor de regras fica em `motor/`.
- Autorização sempre via dependência `exigir_permissao(acao, recurso)` de `app/seguranca/permissoes.py`.
  Nunca verifique perfil com `if` solto na rota.
- Escopo por setor via `escopo_setores(usuario)`, que retorna os setores visíveis (próprio ramo + publicados acima).
- Pydantic v2 para entrada e saída; nunca exponha modelo SQLAlchemy direto.
- Datas de período: `date` no primeiro dia do mês (`2026-10-01`). Fuso `America/Recife` para regras de prazo.
- Eventos de domínio publicados em `app/motor/eventos.py` (`MedicaoRegistrada`, `FarolMudou`, `AcaoVenceu`...);
  reações assíncronas via fila (tabela `fila_tarefa` + worker) até haver necessidade de broker.
- Erros: exceções de domínio em `dominio/erros.py`, mapeadas para HTTP em um único handler.

## Banco
- Nomes de tabela no singular, snake_case, em português. PK `id` UUID v7. `criado_em`, `atualizado_em` em toda tabela.
- `ltree` em `indicador.caminho`; índice GIST. `pgvector` (dimensão definida em F09).
- Toda migração tem `downgrade` funcional.

## Frontend (Next.js + TypeScript)
- App Router, Server Components por padrão; cliente só onde há interação.
- Chamadas à API via cliente gerado do OpenAPI (`frontend/lib/api/`). Nunca `fetch` manual a rotas da API.
- Componentes de domínio em `frontend/components/dominio/` (Farol, ArvoreIndicadores, EspinhaDePeixe...).
- Acessibilidade: farol nunca só por cor; sempre ícone e texto.

## Testes
- Unitários junto ao domínio (`backend/tests/unit`), integração com banco real via Testcontainers.
- Aceitação: `specs/Fxx-*/acceptance.feature` é copiado/linkado para `tests/acceptance/` e executado com pytest-bdd.
- Permissões: `tests/permissions/matriz.yaml` (perfil × ação × esperado) gera testes parametrizados.
- Contrato: Schemathesis sobre `/openapi.json`; schemas MCP comparados com `specs/*/contracts/mcp-tools.json`.

## Git
- Branch por fatia: `fatia/F03-anomalia`. Commits pequenos: `F03: regra abre anomalia no vermelho`.

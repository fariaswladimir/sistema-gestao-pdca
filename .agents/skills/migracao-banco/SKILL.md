---
name: migracao-banco
description: Use ao criar tabelas, colunas, índices ou extensões no PostgreSQL via Alembic.
---

# Migração

1. Altere o modelo em `backend/app/modelos/`.
2. `make migration MSG="Fxx descricao"` para gerar; revise o arquivo gerado à mão.
3. Toda tabela: `id` UUID, `criado_em`, `atualizado_em`. FKs com `ondelete` explícito.
4. Colunas novas em tabela com dados: nullable ou com default; preenchimento em migração separada.
5. `downgrade` funcional. Nunca edite migração já aplicada em outro ambiente.
6. Extensões (`ltree`, `vector`) só com `CREATE EXTENSION IF NOT EXISTS`.

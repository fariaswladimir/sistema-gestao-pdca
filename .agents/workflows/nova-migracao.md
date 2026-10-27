---
description: Criar migração de banco segura.
---

1. Siga a skill `migracao-banco`.
2. Rode `make migrate`, depois `alembic downgrade -1` e `make migrate` de novo para provar o downgrade.

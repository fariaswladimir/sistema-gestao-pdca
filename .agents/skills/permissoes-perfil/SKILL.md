---
name: permissoes-perfil
description: Use ao adicionar ações protegidas, perfis ou regras de escopo por setor.
---

# Permissões

- Ações no formato `recurso:verbo` (`indicador:ler`, `meta:aceitar`, `anomalia:aprovar`).
- Mapa perfil → ações em `backend/app/seguranca/permissoes.py`, espelhando @specs/_perfis-permissoes.md.
- Escopo: `escopo_setores(usuario)` devolve o setor do usuário e descendentes; diretoria, escritório e admin veem tudo.
  Itens publicados (indicadores estratégicos) são visíveis a todos os perfis autenticados.
- `tests/permissions/matriz.yaml`: uma linha por ação × perfil com `permitido: true/false`.
  O gerador cria testes para setor próprio e setor alheio.

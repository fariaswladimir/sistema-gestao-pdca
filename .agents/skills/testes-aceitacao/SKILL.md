---
name: testes-aceitacao
description: Use ao transformar acceptance.feature em testes pytest-bdd executáveis.
---

# Testes de aceitação

- Link simbólico ou cópia de `specs/Fxx-*/acceptance.feature` para `tests/acceptance/Fxx/`.
- Passos em `tests/acceptance/passos/` reutilizáveis entre fatias (ex.: "Dado um indicador {polaridade} com meta {meta}").
- Cada cenário roda contra a API real (TestClient + banco de teste), não contra o serviço direto,
  exceto regras puras do motor.
- Usuários de teste por perfil em `tests/fixtures/usuarios.py` (um por perfil e por setor A/B).
- Nunca use `skip` para fazer a fatia passar. Cenário impossível = conversar com o humano.

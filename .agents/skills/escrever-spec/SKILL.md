---
name: escrever-spec
description: Use ao criar ou revisar spec.md e acceptance.feature de uma fatia do Sistema de Gestão PDCA/SDCA.
---

# Escrever spec de fatia

Uma boa spec descreve comportamento observável e cabe em uma ou duas páginas.

- Objetivo em uma frase, do ponto de vista do usuário.
- Histórias no formato "Como <perfil>, quero <ação> para <resultado>". Use só perfis de `_perfis-permissoes.md`.
- Regras de negócio numeradas (RN1, RN2...). Cada regra precisa aparecer em pelo menos um cenário.
- Cenários Gherkin em português (`# language: pt`, palavras-chave Funcionalidade, Cenário, Dado, Quando, Então, E).
  Valores concretos: "meta 80%", "medição 72%", "período 2026-10".
- Sempre inclua: um caminho feliz, um caso de borda, uma permissão negada, uma auditoria verificada.
- Fora do escopo explícito, apontando para a fatia que fará.
- Questões em aberto com [DECIDIR]; nunca resolva uma por conta própria.
- Não cite tecnologia (banco, framework) na spec; isso vai para o plan.

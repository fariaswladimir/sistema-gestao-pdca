---
trigger: model_decision
description: Aplicar ao criar ou alterar endpoints, ferramentas MCP, consultas, autenticação, perfis, auditoria ou dados de colaboradores.
---

# Segurança, perfis e auditoria

> **Vigência (2026-10-28):** autenticação real só a partir da fatia [DECIDIR: F02 ou F03], com modo local
> (`AUTH_MODO=local`) até lá; perfis, escopo e testes de permissão só nas versões finais (F09/F10).
> Auditoria das escritas, segredos fora do código e LGPD nos logs valem desde já. Ver "Diretrizes de versão" no AGENTS.md.

- Perfis: admin, escritorio, diretoria, gestor, colaborador, leitor, servico. Matriz em @specs/_perfis-permissoes.md.
- Autenticação: OIDC via Keycloak em todos os ambientes; na v1, usuários com login e senha próprios no Keycloak (sem SSO corporativo; federação com Entra ID fica para depois). API externa: OAuth 2.0 client credentials
  com escopos. MCP: OAuth com o token do usuário conectado; a IA herda exatamente as permissões dele.
- Toda rota nova: dependência de permissão + teste positivo e negativo na matriz.
- Toda consulta de listagem aplica `escopo_setores`. Teste com usuário de outro setor é obrigatório.
- Auditoria: `registrar_auditoria(entidade, id, acao, antes, depois, ator)`; para IA, preencher `ator_tipo='ia'`
  e `modelo_ia`.
- Webhooks: assinatura HMAC-SHA256 no cabeçalho `X-Assinatura`, com timestamp; segredo por assinatura.
- Nunca registre em log: e-mail, valores de metas individuais, conteúdo de prompts com dados pessoais, tokens.

---
trigger: model_decision
description: Aplicar ao criar ou alterar endpoints, ferramentas MCP, consultas, autenticação, perfis, auditoria ou dados de colaboradores.
---

# Segurança, perfis e auditoria

- Perfis: admin, escritorio, diretoria, gestor, colaborador, leitor, servico. Matriz em @specs/_perfis-permissoes.md.
- Autenticação: OIDC (Keycloak local; Microsoft Entra ID em produção). API externa: OAuth 2.0 client credentials
  com escopos. MCP: OAuth com o token do usuário conectado; a IA herda exatamente as permissões dele.
- Toda rota nova: dependência de permissão + teste positivo e negativo na matriz.
- Toda consulta de listagem aplica `escopo_setores`. Teste com usuário de outro setor é obrigatório.
- Auditoria: `registrar_auditoria(entidade, id, acao, antes, depois, ator)`; para IA, preencher `ator_tipo='ia'`
  e `modelo_ia`.
- Webhooks: assinatura HMAC-SHA256 no cabeçalho `X-Assinatura`, com timestamp; segredo por assinatura.
- Nunca registre em log: e-mail, valores de metas individuais, conteúdo de prompts com dados pessoais, tokens.

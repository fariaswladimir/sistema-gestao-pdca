---
description: Revisão de segurança, perfis e LGPD do diff da fatia.
---

1. Liste os arquivos alterados em relação à branch principal.
2. Para cada endpoint e ferramenta MCP novo ou alterado, verifique:
   dependência `exigir_permissao`, aplicação de `escopo_setores`, linha na matriz de permissões, auditoria em escritas.
3. Procure dados pessoais em logs, mensagens de erro, fixtures e prompts.
4. Verifique se escritas de IA nascem como rascunho/pendente.
5. Verifique segredos no diff e assinatura de webhooks quando houver.
6. Produza um relatório: achados (crítico, alto, médio), arquivo e linha, correção sugerida. Não corrija sem pedir.

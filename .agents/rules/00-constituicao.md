---
trigger: always_on
---

# Constituição do projeto (vale para toda fatia e toda tarefa)

1. **Spec antes de código.** Só implemente o que está em `specs/Fxx-*/spec.md` com status Aprovada.
   Ambiguidade na spec: pare e pergunte. Não invente regra de negócio.
2. **A spec manda nos testes, não o contrário.** Se um teste de aceitação não passa, corrija o código.
   Mudar `spec.md` ou `acceptance.feature` exige aprovação explícita do humano.
3. **Fatia vertical e pequena.** Cada tarefa de `tasks.md` deixa o sistema funcionando e testado.
   Não antecipe funcionalidade de fatias futuras; deixe um TODO com o código da fatia (ex.: `# TODO(F09)`).
4. **Perfis e escopo só nas versões finais (F09/F10).** Até lá, todo usuário vê e altera tudo e não se criam
   regras de perfil ou escopo novas (ver "Diretrizes de versão" no AGENTS.md). A partir delas: toda leitura filtra
   por perfil e setor (ver @specs/_perfis-permissoes.md) e teste de permissão é obrigatório para todo endpoint
   e ferramenta MCP.
5. **Toda escrita é auditada.** Mudanças em meta, aceite, medição, anomalia, plano, padrão e nota de diagnóstico
   geram `evento_auditoria` com ator, tipo de ator (humano, servico, ia) e antes/depois.
6. **IA nunca decide sozinha.** Tudo o que um modelo de IA cria entra como rascunho ou sugestão pendente,
   com as evidências usadas. Só um humano com perfil adequado aprova.
7. **Dados pessoais (LGPD).** Metas individuais e dados de colaborador só para o próprio, o gestor e o escritório
   de gestão. Nada de dado pessoal em logs, prompts de exemplo ou fixtures reais.
8. **Migrações são imutáveis.** Nunca edite uma migração já aplicada; crie outra.
9. **Segredos fora do código.** Use variáveis de ambiente (`.env`, nunca versionado). Bloqueie commit com segredo.
10. **Pronto = `make check` verde + cenários da fatia verdes + demo descrita em `walkthrough`.**
11. **Linguagem do domínio em português** em tabelas, entidades, rotas e ferramentas MCP
    (indicador, medicao, anomalia). Código de infraestrutura segue convenções em inglês do framework.
12. Ao terminar uma tarefa, atualize a caixa correspondente em `tasks.md` e registre decisões técnicas
    relevantes em `specs/Fxx-*/decisoes.md`.

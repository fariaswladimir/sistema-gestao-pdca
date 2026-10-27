# F07 – MCP de leitura

Status: Rascunho · Release: R3 · Depende de: F06

## Objetivo
Qualquer modelo de IA compatível com MCP (Claude, Gemini e outros) consegue consultar a gestão em linguagem natural,
com exatamente as permissões de quem está conectado. Exemplo: "como está o meu setor este mês?".

## Perfis envolvidos
Todos os perfis autenticados (cada um vê o próprio escopo); admin habilita o servidor.

## Histórias
1. Como colaborador, quero conectar meu assistente de IA ao sistema e perguntar sobre meus indicadores, metas e ações.
2. Como gestor, quero perguntar à IA quais indicadores do setor estão fora do alvo e por quê (anomalias e causas registradas).
3. Como qualquer perfil, quero que a IA encontre POPs e lições aprendidas relevantes.
4. Como admin, quero ver quais modelos e usuários acessaram o servidor MCP e quando.

## Regras de negócio
RN1. Servidor MCP em `/mcp` (Streamable HTTP), autenticado por OAuth 2.0 com o usuário; sem token, nenhuma ferramenta responde.
RN2. Ferramentas desta fatia são só de leitura: consultar_arvore, consultar_indicador, listar_pendencias, consultar_padroes.
RN3. As respostas aplicam o mesmo escopo e privacidade da API (metas individuais, setores).
RN4. Todo acesso é auditado com usuário, ferramenta, canal mcp e cliente (nome declarado pelo cliente MCP).
RN5. Recursos MCP de leitura: arvore://objetivo/{id}, pop://{id}. Prompt: "resumo_do_setor".
RN6. Respostas trazem texto curto legível e dados estruturados; listas limitadas a 50 itens com paginação.

## Fora do escopo
Ferramentas de escrita e sugestões (F09), diagnóstico (consultar_diagnostico entra na F08).

## Impacto em API e MCP
Novo endpoint MCP; schemas em `contracts/mcp-tools.json`.

## Pronto quando
Um usuário do piloto conecta um cliente MCP (ex.: Claude ou Gemini no Antigravity) e obtém a situação do seu setor,
sem ver nada fora do seu escopo.

## Questões em aberto
- [DECIDIR] Quais clientes MCP serão homologados primeiro?

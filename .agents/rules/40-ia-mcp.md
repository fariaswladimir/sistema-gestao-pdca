---
trigger: glob
globs: backend/app/mcp/**, backend/app/ia/**, tests/evals/**
---

# IA e MCP

- O servidor MCP expõe ferramentas com nomes em português snake_case (`consultar_arvore`, `abrir_anomalia`).
  O schema de cada ferramenta é contrato: fica em `specs/Fxx-*/contracts/mcp-tools.json` e tem teste.
- Toda ferramenta MCP: (1) valida entrada com Pydantic, (2) chama o MESMO serviço usado pela API,
  (3) aplica permissão do usuário conectado, (4) audita, (5) devolve texto curto + dados estruturados.
- Ferramentas de escrita criam rascunho/sugestão pendente. Nenhuma ferramenta aprova, fecha ou apaga.
- O agente interno de IA usa as ferramentas MCP do próprio sistema, não acessa o banco direto.
- Toda sugestão de IA guarda: evidências (ids e trechos), modelo, versão do prompt e status (pendente, aceita, descartada).
- Provedor de modelo atrás de `app/ia/gateway.py` (trocável por configuração). Prompts versionados em `app/ia/prompts/`.
- Mudança em prompt ou modelo exige rodar `make evals` e anexar o resultado ao walkthrough.

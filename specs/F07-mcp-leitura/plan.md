# F07 – Plano

## Componentes
- `mcp/servidor.py`: servidor com SDK oficial `mcp` (FastMCP), montado no app FastAPI em `/mcp`.
- `mcp/base.py`: decorator `@ferramenta(nome, acao, escrita)` que resolve usuário pelo token, aplica permissão, abre sessão,
  audita (canal mcp, cliente declarado) e formata resposta (texto + structuredContent).
- `mcp/ferramentas/`: uma por arquivo, todas chamando serviços existentes (F01 a F04).
- OAuth: o servidor MCP atua como resource server; tokens emitidos pelo IdP (Keycloak/Entra) com audience do MCP.
- Paginação por cursor em listas.

## Testes
- Contrato: ferramentas listadas pelo servidor batem com `contracts/mcp-tools.json` (nome, descrição, schema).
- Cliente MCP de teste (SDK) contra o servidor em teste, com usuários por perfil e setor.
- Aceitação e permissões (setor alheio, metas individuais).

## Riscos
Clientes MCP com suporte variado a OAuth: documentar configuração para os clientes homologados em `docs/mcp-clientes.md`.

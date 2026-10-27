# F08 – Plano

## Modelo de dados
`item_diagnostico`, `diagnostico`, `resultado_item`, `autodiagnostico`; marca em `indicador` (`papel = 'indice_execucao_gestao'`).

## Motor
- `motor/diagnostico/`: uma regra pura por item automático (A1 a A6), recebendo dados do período e devolvendo nota e evidências.
- Recalcular nota parcial em eventos relevantes e no job diário (cache em `resultado_item` com origem regra).
- Fechamento: transação que congela resultados e grava a medição do indicador estratégico via serviço de medição.

## API
| Método | Rota | Permissão |
| --- | --- | --- |
| GET/POST/PATCH | /itens-diagnostico | diagnostico:avaliar |
| GET | /diagnosticos?setor=&periodo= | diagnostico:ler |
| POST | /diagnosticos (abrir período) | diagnostico:avaliar |
| PUT | /diagnosticos/{id}/itens/{item} | diagnostico:avaliar |
| POST | /diagnosticos/{id}/fechar, /reabrir | diagnostico:avaliar |
| POST/GET | /setores/{id}/autodiagnosticos | ritual:conduzir / diagnostico:ler |

## MCP
`consultar_diagnostico` (leitura) adicionada ao contrato da F07 (atualizar `F07-mcp-leitura/contracts/mcp-tools.json`).

## Telas
Painel do diagnóstico por setor (nota, itens, evidências clicáveis), tela de avaliação do escritório, autodiagnóstico.

## Testes
Regras A1 a A6 com tabelas de casos, não aplicável, fechamento e imutabilidade, alimentação do indicador, aceitação, permissões, contrato MCP.

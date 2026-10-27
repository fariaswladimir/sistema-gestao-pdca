# F06 – Plano

## Modelo de dados
`credencial_api`, `integracao`, `mapeamento_fonte`, `webhook_assinatura`, `webhook_entrega`.

## Componentes
- `seguranca/oauth.py`: token endpoint client credentials; escopos como ações da matriz.
- `integracoes/jira.py`: cliente com timeout, retry e limite de taxa; `integracoes/transformacoes.py` (contagem, percentual, soma).
- `motor/regras/coleta.py`: agendamento por mapeamento; grava medição via o mesmo serviço do lançamento manual.
- `webhooks/`: assinante de eventos de domínio, fila de entrega, assinatura HMAC, backoff.
- Segredos: referência a cofre/variável de ambiente; nunca no banco em claro.

## API
| Método | Rota | Permissão |
| --- | --- | --- |
| POST | /oauth/token | credencial válida |
| GET/POST/DELETE | /credenciais | credencial_api:gerir |
| GET/POST/PATCH | /integracoes | integracao:gerir |
| POST | /integracoes/{id}/testar | integracao:gerir |
| GET/POST/PATCH | /indicadores/{id}/fonte | indicador:desdobrar (escritório) |
| POST | /indicadores/{id}/coletar?periodo= | indicador:desdobrar |
| GET/POST/DELETE | /webhooks, GET /webhooks/{id}/entregas | integracao:gerir |

## Contratos
`contracts/webhook-eventos.json`: schema de cada evento. OpenAPI gerado e validado por Schemathesis.

## Testes
Jira simulado (respx), HMAC com vetor de teste fixo, backoff com relógio controlado, contrato OpenAPI, aceitação, permissões.

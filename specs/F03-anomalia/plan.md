# F03 – Plano

## Modelo de dados
`anomalia`, `causa`, `plano_acao`, `acao`, `verificacao_eficacia`, `aviso` (central de avisos: destinatario_id, tipo, ref, lido_em).

## Regras de domínio e motor
- `dominio/anomalias.py`: máquina de estados com transições permitidas e pré-condições (RN2 a RN7).
- `motor/regras/abrir_anomalia.py`: reage a `FarolMudou` (para vermelho) em item de controle; idempotente por (indicador, período).
- `motor/regras/prazos.py`: job diário (America/Recife) que emite `AcaoVencendo` e `AcaoVenceu`.
- `motor/regras/eficacia.py`: reage a `MedicaoRegistrada` do período seguinte de anomalias em_verificacao.
- `notificacoes/`: canal e-mail + central de avisos; interface pronta para Teams (F05/F06).

## API
| Método | Rota | Permissão |
| --- | --- | --- |
| GET | /anomalias?setor=&status= | indicador:ler (escopo) |
| POST | /anomalias | anomalia:criar |
| GET/PATCH | /anomalias/{id} | anomalia:editar |
| POST | /anomalias/{id}/transicoes | anomalia:editar (aprovar: anomalia:aprovar) |
| POST/PATCH/DELETE | /anomalias/{id}/causas | anomalia:editar |
| POST | /anomalias/{id}/causas/{cid}/raiz | anomalia:aprovar |
| POST/PATCH | /anomalias/{id}/plano, /planos/{id}/acoes | plano:gerir |
| PATCH | /acoes/{id} | acao:atualizar |
| POST | /anomalias/{id}/verificacao | anomalia:aprovar |
| GET | /avisos, POST /avisos/{id}/lido | autenticado |

## Telas
- Lista de anomalias do setor com status.
- Detalhe da anomalia: linha do tempo, espinha de peixe (6 colunas 6M com cartões), plano com ações, verificação.
- "Minhas ações" e central de avisos.

## Testes
Unitário da máquina de estados (todas as transições válidas e inválidas), regras idempotentes, job de prazos com relógio
controlado, aceitação, permissões, E2E do ciclo completo.

## Riscos
Fuso e "dia seguinte" em prazos: relógio injetável e testes com datas fixas.

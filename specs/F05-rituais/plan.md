# F05 – Plano

## Modelo de dados
`tipo_ritual` (regras_pauta em json declarativo), `ritual`, `decisao`, `presenca`, `recorrencia_ritual` (regra RRULE simplificada).

## Regras de domínio e motor
- `dominio/pauta.py`: geradores por tipo de item (indicadores_fora_do_alvo, anomalias_sem_raiz, acoes_vencidas,
  metas_pendentes, dtos_atrasados), combinados pelas regras do tipo de ritual.
- `motor/regras/rituais.py`: gerar ocorrências recorrentes; marcar não realizado no job diário.

## API
| Método | Rota | Permissão |
| --- | --- | --- |
| GET/POST/PATCH | /tipos-ritual | objetivo:gerir (escritório) |
| GET/POST | /rituais?setor=&de=&ate= | ritual:conduzir (GET: indicador:ler) |
| POST | /rituais/{id}/iniciar (gera pauta), /rituais/{id}/pauta/regenerar | ritual:conduzir |
| PUT | /rituais/{id}/ata, /rituais/{id}/presenca | ritual:conduzir |
| POST | /rituais/{id}/decisoes | ritual:conduzir |
| POST | /rituais/{id}/encerrar | ritual:conduzir |

## Telas
Agenda de rituais do setor; tela de condução (pauta à esquerda, ata e decisões à direita, presença no topo);
modo apresentação para tela compartilhada.

## Testes
Geradores de pauta com cenários de dados, fotografia, recorrência, aceitação, permissões, E2E de um ritual completo.

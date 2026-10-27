# F04 – Plano

## Modelo de dados
`padrao` (com versão; tabela `padrao_versao` se preferir histórico separado: registrar em decisoes.md), `verificacao_dto`, `licao`.
`anomalia`: padrao_id opcional.

## Regras de domínio e motor
- `dominio/padroes.py`: versionamento, publicação, obsolescência.
- `motor/regras/agendar_dto.py`: ao publicar e ao registrar DTO.
- `motor/regras/dto_atrasado.py`: no job diário.
- `motor/regras/passagem_sdca_pdca.py`: reage a `DtoRegistrado` e `FarolMudou`.
- `dominio/situacao_sdca.py`: calcula estável / em PDCA / sem padrão.
- Ajustar transição eficaz da F03 para exigir lição e decisão (RN1).

## API
| Método | Rota | Permissão |
| --- | --- | --- |
| GET | /padroes?setor=&indicador= | indicador:ler |
| POST/PATCH | /padroes, /padroes/{id}/versoes | padrao:gerir |
| POST | /padroes/{id}/publicar | padrao:gerir |
| GET | /dtos?status=previsto,atrasado | indicador:ler |
| POST | /padroes/{id}/dtos | dto:registrar |
| POST | /anomalias/{id}/licao | anomalia:aprovar |

## Telas
Biblioteca de POPs do setor (busca, versão vigente, histórico), editor markdown, agenda de DTOs, formulário de DTO,
selo SDCA na árvore e no painel.

## Testes
Versionamento, agendamento com datas fixas, regra de passagem (tabela de casos), aceitação, permissões, E2E anomalia eficaz → POP → DTO.

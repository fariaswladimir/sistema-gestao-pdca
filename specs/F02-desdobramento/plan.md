# F02 – Plano

## Modelo de dados
- `indicador`: pai_id, peso, caminho (ltree), publicado; índice GIST em caminho.
- `aceite_meta`.
- `medicao`: origem `calculado` para pais consolidados.

## Regras de domínio e motor
- `dominio/arvore.py`: validar nível, recalcular caminho ao mover, impedir ciclo.
- `motor/consolidacao.py`: função pura `consolidar(tipo, filhos: list[(valor, peso)])` → valor ou pendência.
- Reação a `MedicaoRegistrada`: recalcular pai e subir até a raiz, no mesmo período, de forma idempotente.

## API
| Método | Rota | Permissão |
| --- | --- | --- |
| POST | /indicadores/{id}/filhos | indicador:desdobrar |
| PATCH | /indicadores/{id}/pai | indicador:desdobrar |
| GET | /objetivos/{id}/arvore?periodo= | indicador:ler (filtrada por escopo) |
| GET | /indicadores/{id}/arvore?periodo= | indicador:ler |
| POST | /metas/{id}/aceite | meta:aceitar |
| POST | /metas/{id}/contestacao | meta:aceitar |
| GET | /metas/pendentes | meta:aceitar |

## Telas
- "Árvore do objetivo": árvore colapsável com farol, valor, meta e indicador de filhos pendentes.
- "Minhas metas" (colaborador) e "Metas da equipe" (gestor) com aceitar/contestar.

## Testes
Unitários de consolidação (todas as regras, pesos, pendências), propagação em 3 níveis, aceitação, permissões
(metas individuais privadas), E2E de desdobrar → lançar filhos → ver pai.

## Riscos
Recalcular ancestrais com muitos nós: fazer em uma transação por período, com consulta por `caminho @>`.

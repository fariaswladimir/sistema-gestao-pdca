# F01 – Plano

## Modelo de dados
- `setor`: adicionar setor_pai_id, gestor_id, unidade, ativo, caminho (ltree) com índice GIST.
- `colaborador`: gestor_id, cargo, status.
- `tipo_indicador`: as 5 dimensões como enums.
- `ciclo`, `objetivo`, `meta` (valor, valor_min, valor_max, periodo opcional).
- `indicador`: tipo_id, objetivo_id, setor_id, responsavel_id, formula_descricao, unidade, periodicidade, tolerancia_pct, ativo.

## Regras de domínio
- `motor/farol.py`: ativar menor_melhor e faixa. `dominio/metas.py`: resolver meta vigente (período > ciclo).
- `dominio/setores.py`: validar hierarquia (sem ciclo), recalcular `caminho` ao mover setor.
- Escopo: `escopo_setores(usuario)` usando `caminho <@ caminho_do_setor`.

## API
| Método | Rota | Permissão |
| --- | --- | --- |
| GET/POST/PATCH | /setores | setor:gerir (GET: autenticado) |
| GET/POST/PATCH | /colaboradores | colaborador:gerir |
| GET/POST/PATCH | /tipos-indicador | tipo_indicador:gerir (GET: autenticado) |
| GET/POST/PATCH | /ciclos, /objetivos | objetivo:gerir |
| POST/PATCH | /indicadores | indicador:desdobrar (estratégicos: indicador:criar_estrategico) |
| PUT | /indicadores/{id}/metas | indicador:desdobrar |
| GET | /paineis/setor/{id}?meses=12 | painel:ler |

## Telas
- Área "Configuração" (escritório): setores (árvore), colaboradores, tipos, ciclos e objetivos, indicadores.
- "Painel do setor": tabela de indicadores com farol, sparkline de 12 meses, filtro por setor descendente.

## Testes
Unitários do farol (tabela completa), domínio de setores, aceitação, permissões das novas ações, E2E de cadastro → painel.

## Riscos
Escopo por ltree mal aplicado vazar dados: teste de setor alheio em toda listagem.

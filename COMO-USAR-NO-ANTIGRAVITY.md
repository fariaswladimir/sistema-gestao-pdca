# Como usar este harness no Google Antigravity

## 1. Abrir o projeto
Abra a pasta raiz no Antigravity. Ele lê automaticamente:
- `AGENTS.md` na raiz (contexto do projeto);
- `.agents/rules/` (regras do workspace);
- `.agents/workflows/` (comandos de barra);
- `.agents/skills/` (skills carregadas sob demanda).

Confira no painel **Customizations** (Rules e Workflows) se os arquivos aparecem. Ajuste a ativação de cada regra se preciso:
- `00-constituicao`, `10-dominio`, `20-stack-convencoes`: Always On
- `30-seguranca`: Model Decision
- `40-ia-mcp`: Glob (`backend/app/mcp/**`, `backend/app/ia/**`)

Versões antigas do Antigravity usam `.agent/` (singular). Se nada aparecer, renomeie `.agents` para `.agent`.

## 2. Configurar MCP do desenvolvimento
Painel do Agent → ⋯ → MCP Servers → Manage MCP Servers → View raw config.
Copie de `.agents/mcp_config.example.json` os servidores que for usar (GitHub, PostgreSQL de dev, Playwright, Atlassian).
A partir da F07, adicione o próprio sistema (`gestao-pdca-local`) para testar como usuário de IA.

## 3. Ciclo de cada fatia
| Passo | Comando no Agent | Você faz |
| --- | --- | --- |
| 1 | `/nova-fatia F00` | Responde os [DECIDIR] e aprova a spec |
| 2 | `/planejar-fatia F00` | Revisa o Implementation Plan |
| 3 | `/implementar-fatia F00` | Acompanha as tarefas; revisa diffs |
| 4 | `/verificar-fatia F00` | Lê o Walkthrough e as evidências |
| 5 | `/demo-fatia F00` | Faz a demo com usuários reais |

Use o modo **Planning** do Agent para as etapas 1 e 2, e permita execução automática de terminal só para
comandos `make` (política de revisão: pedir aprovação para o resto).

## 4. Antes de começar a F00
1. Responda as questões [DECIDIR] da F00 (provedor de identidade e hospedagem).
2. Copie `.env.example` para `.env`.
3. Rode `pre-commit install`.
4. Peça ao Agent: "/nova-fatia F00" e revise.

## 5. Ordem das fatias
F00 → F01 → F02 → F03 (gate G2: PDCA em 1 setor) → F04, F05 e F06 (F06 pode correr em paralelo) →
F07 → F08 → F09 → F10. Detalhes em `specs/README.md`.

## 6. Limites a respeitar
Arquivos de regra e workflow do Antigravity têm limite de 12.000 caracteres. Se crescerem, divida em mais arquivos
e referencie com `@arquivo`.

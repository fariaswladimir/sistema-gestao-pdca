# Specs do Sistema de Gestão PDCA e SDCA

Cada fatia fina tem uma pasta com:

| Arquivo | Conteúdo | Quem aprova |
| --- | --- | --- |
| `spec.md` | O quê e por quê: histórias, regras de negócio, fora do escopo, pronto quando | Humano (dono do produto) |
| `acceptance.feature` | Critérios de aceite em Gherkin, executados como testes | Humano |
| `plan.md` | Como: dados, regras, eventos, API, MCP, telas, testes | Humano revisa |
| `tasks.md` | Passos de 30 min a 2 h, em ordem, com "pronto quando" | Agente mantém |
| `contracts/` | Schemas de ferramentas MCP e trechos de API que são contrato | Humano revisa |
| `decisoes.md` | Decisões técnicas tomadas durante a fatia | Agente registra |

Documentos transversais: `_glossario.md`, `_modelo-dados.md`, `_perfis-permissoes.md`, `_templates/`.

## Releases e status

| Fatia | Release | Nome | Status |
| --- | --- | --- | --- |
| F00 | R0 Esqueleto | Esqueleto andante | Rascunho |
| F01 | R1 MVP PDCA | Meta e farol | Rascunho |
| F02 | R1 MVP PDCA | Desdobramento e aceite | Rascunho |
| F03 | R1 MVP PDCA | Anomalia e plano de ação | Rascunho |
| F04 | R2 Rotina | Rotina SDCA (POP e DTO) | Rascunho |
| F05 | R2 Rotina | Rituais e atas | Rascunho |
| F06 | R2 Rotina | API pública, webhooks e Jira | Rascunho |
| F07 | R3 IA e escala | MCP de leitura | Rascunho |
| F08 | R3 IA e escala | Diagnóstico da gestão | Rascunho |
| F09 | R3 IA e escala | IA sugere (MCP de escrita) | Rascunho |
| F10 | R3 IA e escala | Escala e migração | Rascunho |

Status possíveis: Rascunho → Aprovada → Em implementação → Verificada → Demonstrada.

Gates: **G1** esqueleto no ar (após F00) · **G2** PDCA rodando em 1 setor piloto (após F03) · **G3** rotina sem planilha (após F06).

## Marcadores
- `[DECIDIR]` questão em aberto que só o humano responde. Fatia não é aprovada com [DECIDIR] pendente.
- `[SUPOSIÇÃO]` valor provisório adotado para escrever a spec; confirmar na aprovação.

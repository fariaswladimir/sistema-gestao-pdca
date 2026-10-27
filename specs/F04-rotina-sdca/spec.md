# F04 – Rotina SDCA (POP e DTO)

Status: Rascunho · Release: R2 · Depende de: F03

## Objetivo
Manter o resultado conquistado: a solução eficaz de uma anomalia vira padrão (POP), o sistema agenda verificações de
aderência (DTO) e desvios relevantes devolvem o indicador ao PDCA. Fecha a ponte SDCA ↔ PDCA.

## Perfis envolvidos
gestor, colaborador, escritorio.

## Histórias
1. Como gestor, ao encerrar uma anomalia como eficaz, quero transformar a solução em um POP em rascunho, já ligado ao indicador.
2. Como gestor, quero criar, versionar e publicar POPs das tarefas críticas do setor.
3. Como gestor, quero que o sistema agende DTOs conforme a periodicidade de cada POP e me lembre.
4. Como gestor, quero registrar um DTO (aderente ou não, com desvios) para um colaborador.
5. Como colaborador, quero consultar os POPs vigentes do meu setor.
6. Como gestor, ao encerrar uma anomalia, quero registrar a lição aprendida.

## Regras de negócio
RN1. Encerrar anomalia como eficaz exige registrar a lição aprendida e decidir: criar POP, atualizar POP existente
     ou justificar por que não padronizar.
RN2. POP tem versões; só uma versão vigente por POP. Publicar nova versão torna a anterior obsoleta.
RN3. Cada POP vigente tem periodicidade de DTO (mensal, trimestral, semestral). O sistema agenda o próximo DTO
     ao publicar e ao registrar cada DTO.
RN4. DTO não registrado até 5 dias após a data prevista fica atrasado e gera aviso ao gestor. [SUPOSIÇÃO] 5 dias.
RN5. Regra de passagem SDCA → PDCA: dois DTOs não aderentes seguidos no mesmo POP, ou DTO não aderente no mesmo período
     em que o indicador ligado ficou vermelho, abre anomalia em rascunho (origem regra), vinculada ao POP.
RN6. Situação SDCA de um indicador: "estável" quando está no alvo, sem anomalia aberta e com POP vigente; senão "em PDCA"
     ou "sem padrão". Exibida na árvore e no painel.

## Fora do escopo
Sugestão de POP por IA (F09), DTO no ritual (F05), diagnóstico usando DTO (F08).

## Impacto em API e MCP
Rotas de padrão, versão, DTO, lição. Ferramenta MCP `consultar_padroes` vem na F07.

## Pronto quando
Um padrão nasceu de uma anomalia eficaz no setor piloto e teve ao menos um DTO registrado.

## Questões em aberto
- [DECIDIR] POP precisa de aprovação de alguém acima do gestor (escritório) para ficar vigente?

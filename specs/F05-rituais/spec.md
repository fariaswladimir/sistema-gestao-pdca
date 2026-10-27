# F05 – Rituais e atas

Status: Rascunho · Release: R2 · Depende de: F04

## Objetivo
Os rituais de gestão acontecem dentro do sistema: a pauta chega pronta, mostrando só o que está fora do padrão,
e a reunião termina com ata, decisões que viram ações e presença registrada.

## Perfis envolvidos
gestor, diretoria, escritorio, colaborador (participante).

## Histórias
1. Como escritório, quero configurar tipos de ritual com cadência e regras de pauta.
2. Como gestor, quero agendar rituais recorrentes do meu setor.
3. Como gestor, ao abrir um ritual, quero a pauta gerada por exceção: indicadores vermelhos e amarelos, anomalias sem causa raiz,
   ações vencidas, metas pendentes de aceite e DTOs atrasados.
4. Como gestor, quero registrar a ata, a presença e as decisões; uma decisão pode virar ação com responsável e prazo.
5. Como participante, quero receber a ata e ver as ações que recebi.

## Regras de negócio
RN1. Tipos iniciais: Bom Dia (diária), Reunião de resultados (mensal), Cumbuca (mensal), Feedback (semestral).
RN2. A pauta é uma fotografia: gerada ao abrir o ritual e guardada; pode ser regenerada até o início.
RN3. Pauta da reunião de resultados contém os itens da história 3 do setor e descendentes; da Bom Dia, só ações vencendo
     ou vencidas e avisos do dia.
RN4. Encerrar ritual exige presença registrada. Ata pode ser vazia apenas na Bom Dia.
RN5. Decisão convertida em ação entra no plano de ação da anomalia indicada ou em um plano "ações de ritual" do setor.
RN6. Ritual não realizado até o fim do dia previsto fica "não realizado" (conta para o diagnóstico na F08).

## Fora do escopo
Transcrição automática de reunião e ata por IA (F09), integração com agenda do Outlook/Teams (registrar como evolução).

## Impacto em API e MCP
Rotas de tipo de ritual, ritual, pauta, ata, presença, decisão. `preparar_ritual` no MCP vem na F09.

## Pronto quando
A reunião mensal de resultados do setor piloto acontece só no sistema, sem planilha ou apresentação paralela.

## Questões em aberto
- [DECIDIR] Integrar agendamento com o Outlook já nesta fatia ou depois?

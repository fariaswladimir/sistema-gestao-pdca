# F03 – Anomalia e plano de ação

Status: Rascunho · Release: R1 · Depende de: F02

## Objetivo
Quando um indicador fica vermelho, o setor trata o problema com método (causa raiz e plano de ação),
em vez de só registrar o resultado. Fecha o primeiro ciclo PDCA completo.

## Perfis envolvidos
colaborador, gestor, escritorio; servico (abertura automática).

## Histórias
1. Como gestor, quando o farol fica vermelho, quero que uma anomalia seja aberta em rascunho, para nenhuma meta falhar sem tratamento.
2. Como colaborador, quero abrir uma anomalia manualmente para um problema percebido antes do fechamento.
3. Como colaborador, quero registrar causas na espinha de peixe (6M) e marcar a causa raiz.
4. Como gestor, quero aprovar a causa raiz e criar um plano com ações, responsáveis e prazos.
5. Como responsável por uma ação, quero atualizar o status e ser avisado antes e no vencimento.
6. Como gestor, quero verificar a eficácia no período seguinte e encerrar a anomalia como eficaz ou ineficaz.

## Regras de negócio
RN1. Farol vermelho em item de controle sem anomalia aberta no mesmo indicador e período ⇒ abrir anomalia em rascunho,
     origem "regra", e notificar gestor e responsável. Nunca duplicar.
RN2. Estados: rascunho → em_analise → plano_definido → em_verificacao → eficaz | ineficaz; cancelada a partir de qualquer
     estado não final, com motivo.
RN3. Para sair de em_analise é preciso ao menos uma causa marcada como raiz, aprovada pelo gestor.
RN4. Plano aprovado precisa de ao menos uma ação com responsável e prazo futuro.
RN5. Ação vencida e não concluída gera notificação ao responsável e ao gestor no dia seguinte ao prazo; aviso prévio
     [SUPOSIÇÃO] 2 dias antes.
RN6. Com todas as ações concluídas, a anomalia vai para em_verificacao. A verificação usa a medição do período seguinte:
     se o farol não estiver vermelho, sugere eficaz; o gestor confirma.
RN7. Ineficaz reabre análise (nova rodada de causas e plano), mantendo o histórico.
RN8. Todas as transições são auditadas.

## Fora do escopo
Converter ação eficaz em padrão (F04), lição aprendida (F04), sugestão de causas por IA (F09), notificação por Teams (F05/F06).
Notificação nesta fatia: e-mail e central de avisos no sistema.

## Impacto em API e MCP
Rotas de anomalia, causa, plano, ação, verificação. MCP fica para F07/F09.

## Pronto quando
Um ciclo PDCA real do setor piloto foi aberto e acompanhado até a verificação de eficácia no sistema.

## Questões em aberto
- [DECIDIR] Item de verificação vermelho também abre anomalia automática, ou só item de controle (assumido)?
- [DECIDIR] Amarelo deve gerar alerta sem anomalia?

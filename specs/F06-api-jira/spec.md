# F06 – API pública, webhooks e Jira

Status: Rascunho · Release: R2 · Depende de: F03 (pode correr em paralelo à F04/F05)

## Objetivo
Outros sistemas conversam com a gestão: indicadores são alimentados automaticamente (começando pelo Jira),
sistemas externos são avisados de eventos por webhook, e tudo o que a interface faz está disponível na API.

## Perfis envolvidos
admin (credenciais, integrações), escritorio (mapeia indicador à fonte), servico (credencial técnica).

## Histórias
1. Como admin, quero criar credenciais de API com escopos e setor, com expiração e revogação.
2. Como admin, quero cadastrar uma integração com o Jira (URL e token guardados como segredo).
3. Como escritório, quero ligar um indicador a uma consulta JQL e a uma transformação (contagem, percentual entre duas consultas,
   soma de campo), com agendamento.
4. Como sistema externo, quero assinar eventos por webhook e recebê-los assinados, com novas tentativas em caso de falha.
5. Como desenvolvedor de integração, quero documentação OpenAPI navegável.

## Regras de negócio
RN1. Credencial de serviço nunca tem escopo maior que o do admin que a criou; o segredo é exibido uma única vez.
RN2. Indicador com origem integracao não aceita lançamento manual, exceto correção com justificativa por gestor (auditada).
RN3. A coleta grava a medição do período com origem integracao e dispara os mesmos eventos do lançamento manual
     (farol, consolidação, anomalia).
RN4. Falha de coleta não apaga valor anterior; gera aviso ao escritório e registra erro na integração.
RN5. Eventos de webhook: medicao.registrada, farol.vermelho, anomalia.aberta, acao.vencida, ritual.encerrado.
RN6. Entrega de webhook assinada com HMAC-SHA256 (cabeçalhos X-Assinatura e X-Timestamp), até 5 tentativas com espera
     exponencial; depois marcada como falha. [SUPOSIÇÃO] 5 tentativas.
RN7. Payload de webhook nunca leva meta individual nem dados pessoais além de ids.

## Fora do escopo
Microsoft 365 e ERP (evolução após F06, mesmo padrão de conector), MCP (F07).

## Impacto em API e MCP
Documentação OpenAPI pública em `/docs`; rotas de credencial, integração, mapeamento, assinatura e entregas.

## Pronto quando
Pelo menos um indicador do piloto é alimentado pelo Jira sem digitação manual, e um sistema externo recebe o webhook de farol vermelho.

## Questões em aberto
- [DECIDIR] Jira Cloud ou Data Center? Autenticação por token de API ou OAuth?
- [DECIDIR] Frequência de coleta padrão (assumido: diária às 6h e no último dia do mês).

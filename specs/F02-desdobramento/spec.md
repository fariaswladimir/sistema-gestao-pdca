# F02 – Desdobramento e aceite de metas

Status: Rascunho · Release: R1 · Depende de: F01

## Objetivo
A diretoria desdobra um objetivo estratégico até setores, times e pessoas; o resultado dos filhos compõe o pai
automaticamente; e cada meta só vale depois de aceita pelo responsável e pelo gestor.

## Perfis envolvidos
diretoria, escritorio, gestor, colaborador.

## Histórias
1. Como diretoria, quero criar indicadores estratégicos ligados a objetivos e publicá-los para toda a organização.
2. Como gestor, quero desdobrar um indicador em indicadores filhos para setores, times ou pessoas, com peso quando necessário.
3. Como qualquer perfil, quero ver a árvore de um objetivo com o farol de cada nó.
4. Como colaborador, quero aceitar ou contestar a meta que recebi, com comentário.
5. Como gestor, quero aceitar as metas da equipe e ver quais estão pendentes.

## Regras de negócio
RN1. Indicador estratégico não tem pai e pertence a um objetivo. Os demais têm exatamente um pai.
RN2. O nível do filho é igual ou inferior ao do pai (estratégico > setor > time > individual).
RN3. Consolidação do pai segue o tipo do pai: soma, media, media_ponderada (pelos pesos), ultimo, nenhuma.
     Com consolidação diferente de nenhuma, o valor do pai é calculado e não pode ser lançado à mão.
RN4. O valor consolidado do período só é calculado quando todos os filhos ativos têm medição; senão o pai fica sem_dado
     e mostra quantos filhos faltam.
RN5. Mudança em medição de filho recalcula pai e ancestrais no mesmo período.
RN6. Meta de indicador individual ou de time tem status pendente até ter aceite do responsável e do gestor.
     Contestação volta ao gestor com comentário obrigatório.
RN7. Meta individual só é visível ao próprio, ao gestor do setor, ao escritório e ao admin.
RN8. Indicadores publicados (estratégicos) são visíveis a todos os autenticados.
RN9. Mover um nó de pai é auditado e recalcula consolidação.

## Fora do escopo
Anomalias (F03), importação de árvore por planilha (F10).

## Impacto em API e MCP
`POST /indicadores/{id}/filhos`, `GET /objetivos/{id}/arvore`, `GET /indicadores/{id}/arvore`,
`POST /metas/{id}/aceite`, `POST /metas/{id}/contestacao`, `GET /metas/pendentes`. Sem MCP.

## Pronto quando
Um objetivo real está desdobrado até o setor piloto, o farol do pai reflete os filhos e os aceites estão registrados.

## Questões em aberto
- [DECIDIR] Pai com filhos faltando: mostrar sem_dado (assumido) ou consolidar parcial com aviso?
- [DECIDIR] Aceite também para metas de setor, ou só time e individual (assumido)?

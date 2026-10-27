# language: pt
Funcionalidade: Rotina SDCA

  Contexto:
    Dado o indicador "IND-10" do setor "Piloto", gestor "carlos", com a anomalia "A-01" em "em_verificacao"

  Cenário: encerrar eficaz exige lição e decisão de padronização
    Quando "carlos" confirma "A-01" como eficaz sem lição aprendida
    Então recebe resposta 422
    Quando ele confirma com a lição "checar roteiro antes da visita" e a decisão "criar POP"
    Então "A-01" fica "eficaz"
    E existe um POP "rascunho" ligado a "IND-10" com origem "A-01"

  Cenário: publicar nova versão torna a anterior obsoleta
    Dado o POP "POP-07" versão 1 vigente
    Quando "carlos" publica a versão 2
    Então a versão 2 está "vigente" e a versão 1 "obsoleto"

  Cenário: DTO agendado ao publicar
    Dado o POP "POP-07" com periodicidade mensal publicado em "2026-11-03"
    Então existe DTO previsto para "2026-12-03"

  Cenário: DTO atrasado gera aviso
    Dado o DTO de "POP-07" previsto para "2026-12-03" não registrado
    Quando o dia "2026-12-09" é processado
    Então "carlos" recebe aviso de DTO atrasado

  Cenário: dois DTOs não aderentes seguidos voltam ao PDCA
    Dado o DTO anterior de "POP-07" não aderente
    Quando "carlos" registra um novo DTO de "POP-07" não aderente com desvio "etapa 3 pulada"
    Então existe anomalia "rascunho" de origem "regra" vinculada a "POP-07" e "IND-10"

  Cenário: situação SDCA estável
    Dado "IND-10" verde no período, sem anomalia aberta e com "POP-07" vigente
    Quando a árvore é consultada
    Então "IND-10" aparece com situação "estável"

  Cenário: colaborador não edita POP
    Dado "ana" com perfil colaborador
    Quando ela tenta editar "POP-07"
    Então recebe resposta 403
    Mas ela consegue ler a versão vigente de "POP-07"

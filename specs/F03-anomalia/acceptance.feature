# language: pt
Funcionalidade: Anomalia e plano de ação

  Contexto:
    Dado o item de controle "IND-10" do setor "Piloto", "maior_melhor", meta 80, responsável "ana", gestor "carlos"

  Cenário: farol vermelho abre anomalia em rascunho
    Quando é lançado 72 em "IND-10" no período "2026-10"
    Então existe uma anomalia "rascunho" de origem "regra" ligada a "IND-10" e "2026-10"
    E "carlos" e "ana" recebem aviso

  Cenário: não duplica anomalia no mesmo período
    Dado uma anomalia aberta para "IND-10" em "2026-10"
    Quando o valor de "IND-10" em "2026-10" é corrigido para 70 com justificativa
    Então continua existindo uma única anomalia para "IND-10" em "2026-10"

  Cenário: análise exige causa raiz aprovada
    Dado a anomalia de "IND-10" em "em_analise" com 3 causas e nenhuma raiz
    Quando "carlos" tenta definir o plano
    Então recebe resposta 409 com a mensagem "causa raiz não aprovada"

  Cenário: plano exige ação com prazo futuro
    Dado a anomalia com causa raiz aprovada
    Quando "carlos" aprova um plano sem ações
    Então recebe resposta 422

  Cenário: ação vencida gera aviso
    Dado a ação "Revisar roteiro" de "ana" com prazo "2026-11-10" e status "aberta"
    Quando o dia "2026-11-11" é processado
    Então "ana" e "carlos" recebem aviso de ação vencida

  Cenário: verificação sugere eficácia pelo período seguinte
    Dado a anomalia de "IND-10" em "2026-10" com todas as ações concluídas
    Quando é lançado 83 em "IND-10" no período "2026-11"
    Então a anomalia sugere "eficaz"
    Quando "carlos" confirma
    Então a anomalia fica "eficaz"

  Cenário: ineficaz reabre análise com histórico
    Dado a anomalia em "em_verificacao"
    Quando "carlos" registra "ineficaz"
    Então a anomalia volta a "em_analise" e mantém as causas e o plano anteriores no histórico

  Cenário: colaborador não aprova causa raiz
    Dado "ana" com perfil colaborador
    Quando ela tenta aprovar a causa raiz
    Então recebe resposta 403

  Cenário: setor alheio não vê a anomalia
    Dado "duda" colaboradora de outro setor
    Quando ela consulta a anomalia de "IND-10"
    Então recebe resposta 404

  Cenário: transições auditadas
    Quando a anomalia passa de "rascunho" para "em_analise" por "carlos"
    Então existe evento de auditoria com estado anterior, novo e ator "carlos"

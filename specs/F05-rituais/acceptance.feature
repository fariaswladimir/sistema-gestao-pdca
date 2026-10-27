# language: pt
Funcionalidade: Rituais e atas

  Contexto:
    Dado o setor "Piloto" com gestor "carlos" e colaboradores "ana" e "bruno"

  Cenário: pauta por exceção da reunião de resultados
    Dado no período "2026-10" o indicador "IND-10" vermelho e "IND-11" verde
    E a anomalia de "IND-10" sem causa raiz
    E a ação "Revisar roteiro" de "ana" vencida
    Quando "carlos" abre a reunião de resultados de "2026-11-05"
    Então a pauta contém "IND-10", a anomalia sem causa raiz e a ação vencida
    E a pauta não contém "IND-11"

  Cenário: pauta é fotografia
    Dado a pauta gerada às 09:00
    Quando "IND-11" fica vermelho às 09:30
    Então a pauta guardada não muda até "carlos" pedir para regenerar

  Cenário: decisão vira ação
    Dado o ritual em andamento
    Quando "carlos" registra a decisão "treinar equipe no POP-07" como ação de "bruno" com prazo "2026-11-20"
    Então "bruno" tem a ação "treinar equipe no POP-07" em suas ações

  Cenário: encerrar exige presença
    Quando "carlos" tenta encerrar o ritual sem presença
    Então recebe resposta 422

  Cenário: ritual não realizado
    Dado a Bom Dia de "2026-11-06" agendada e não iniciada
    Quando o dia "2026-11-07" é processado
    Então o ritual fica "não realizado"

  Cenário: colaborador não conduz ritual
    Quando "ana" tenta encerrar o ritual
    Então recebe resposta 403

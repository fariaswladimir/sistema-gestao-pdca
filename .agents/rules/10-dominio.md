---
trigger: always_on
---

# Domínio (resumo; detalhes em @specs/_glossario.md e @specs/_modelo-dados.md)

- **Árvore de desdobramento:** objetivo estratégico → indicador estratégico → indicador de setor → time → individual.
  Cada indicador tem um nó pai (exceto os estratégicos) e um caminho `ltree`.
- **Tipo de indicador** classifica em 5 dimensões: nível, natureza (item de controle ou item de verificação),
  polaridade (maior_melhor, menor_melhor, faixa), consolidação (soma, media, media_ponderada, ultimo, nenhuma),
  origem (manual, integracao, calculado). O tipo decide farol e consolidação.
- **Farol:** verde, amarelo, vermelho, sem_dado. Calculado pelo motor de regras em `backend/app/motor/farol.py`.
  Nunca calcule farol em outro lugar.
- **SDCA:** indicador no alvo e com padrão (POP) roda manutenção: padrão → execução → verificação (DTO) → correção.
- **PDCA:** meta nova, resultado fora do alvo ou tarefa sem padrão: anomalia → causas (6M) → causa raiz →
  plano de ação → verificação de eficácia → padronização (vira POP) e lição aprendida.
- **Regra de passagem:** vermelho sem anomalia aberta no período ⇒ abrir anomalia em rascunho (origem `regra`).
  Ação eficaz ⇒ padrão e volta ao SDCA. Desvio de DTO repetido ou que derruba o indicador ⇒ PDCA.
- **Rituais:** Bom Dia, reunião de resultados, Cumbuca, feedback. Pauta gerada por exceção.
- **Diagnóstico da gestão:** itens com regra automática ou avaliação manual; nota por setor e período;
  a média alimenta o indicador estratégico "Índice de execução da gestão".

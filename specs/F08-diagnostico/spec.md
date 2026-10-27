# F08 – Diagnóstico da gestão

Status: Rascunho · Release: R3 · Depende de: F05 (usa rituais, DTOs, anomalias e planos)

## Objetivo
A prática do método em cada setor é avaliada continuamente: itens verificáveis por dados são calculados pelo sistema,
o avaliador revisa só o que exige julgamento, e a nota alimenta o indicador estratégico de execução da gestão.

## Perfis envolvidos
escritorio (configura itens, avalia e fecha), gestor e colaborador (leem e fazem autodiagnóstico), diretoria (lê).

## Histórias
1. Como escritório, quero configurar itens de diagnóstico com critério, tipo (automático ou manual), regra e peso.
2. Como gestor, quero ver a nota parcial do meu setor a qualquer momento e o que falta para melhorar.
3. Como escritório, quero abrir o diagnóstico do quadrimestre, avaliar os itens manuais e fechar com a nota final.
4. Como gestor, quero fazer um autodiagnóstico mensal com a equipe.
5. Como diretoria, quero que a média das notas alimente o indicador estratégico de execução da gestão.

## Regras de negócio
RN1. Itens automáticos iniciais (nota 0 a 100):
     A1 todo indicador vermelho no período tem anomalia aberta no mesmo mês;
     A2 percentual de ações do setor sem atraso;
     A3 percentual de medições lançadas até o dia 5 do mês seguinte [SUPOSIÇÃO dia 5, como na FIEPE];
     A4 percentual de rituais previstos realizados com presença;
     A5 percentual de DTOs realizados no prazo;
     A6 percentual de metas do setor aceitas.
RN2. Itens manuais exigem avaliador do escritório, nota e comentário.
RN3. Nota do setor = média ponderada dos itens pelo peso. Item sem base de cálculo (ex.: nenhum indicador vermelho)
     vale 100 e mostra "não aplicável no período".
RN4. Diagnóstico tem período (padrão quadrimestral), fica aberto com nota parcial calculada continuamente e é fechado pelo escritório;
     depois de fechado, é imutável (correção só com reabertura auditada).
RN5. Ao fechar o diagnóstico de todos os setores do período, a média ponderada das notas vira a medição do indicador estratégico
     marcado como "índice de execução da gestão".
RN6. Cada item mostra as evidências (ids de indicadores, ações, rituais) que geraram a nota.
RN7. Autodiagnóstico não altera a nota oficial; fica como histórico do setor.

## Fora do escopo
Pré-diagnóstico escrito por IA (F09).

## Impacto em API e MCP
Rotas de item, diagnóstico, avaliação, fechamento, autodiagnóstico. Ferramenta MCP de leitura `consultar_diagnostico`.

## Pronto quando
O diagnóstico do setor piloto é fechado sem auditoria manual nos itens automáticos, e o indicador estratégico recebe a nota.

## Questões em aberto
- [DECIDIR] Pesos iniciais dos itens (assumido: todos iguais).
- [DECIDIR] Lista de itens manuais (ex.: qualidade das análises de causa, uso da Gestão à Vista).

# F09 – IA sugere (MCP de escrita)

Status: Rascunho · Release: R3 · Depende de: F07, F08 e histórico de anomalias suficiente

## Objetivo
A IA acelera o PDCA: sugere causas prováveis e rascunha planos, pautas e atas, sempre mostrando as evidências que usou,
e nada vale sem aprovação humana. Modelos externos passam a poder escrever no sistema via MCP, sempre como rascunho.

## Perfis envolvidos
colaborador, gestor (usam e decidem sugestões), escritorio (acompanha qualidade), admin (configura provedor).

## Histórias
1. Como colaborador, ao analisar uma anomalia, quero ver causas prováveis com base em anomalias parecidas, POPs e lições,
   com os casos citados.
2. Como gestor, quero um rascunho de plano de ação a partir da causa raiz aprovada.
3. Como gestor, quero um rascunho de ata a partir das anotações do ritual e das decisões.
4. Como usuário de um assistente externo, quero registrar medição, abrir anomalia e pedir sugestões via MCP.
5. Como escritório, quero acompanhar a taxa de aceitação e a avaliação das sugestões por tipo.

## Regras de negócio
RN1. Toda sugestão é guardada como `sugestao_ia` pendente, com evidências (ids e trechos), modelo e versão do prompt.
RN2. Aceitar uma sugestão cria o objeto correspondente (causa, ação, ata) com origem ia e autor humano que aceitou;
     o usuário pode editar antes de aceitar (status aceita_editada).
RN3. A busca de evidências respeita o escopo do usuário: nunca usa anomalias, POPs ou atas de setores que ele não vê.
RN4. Sem evidência suficiente (menos de 2 casos parecidos), a IA diz isso em vez de inventar causa. [SUPOSIÇÃO] limiar 2.
RN5. Ferramentas MCP de escrita: registrar_medicao, abrir_anomalia, sugerir_causas, criar_plano_acao, preparar_ritual.
     Medição via MCP segue as mesmas regras da API; abrir_anomalia, criar_plano_acao e preparar_ritual criam rascunho.
RN6. Nenhuma ferramenta MCP aprova, encerra, exclui ou altera meta.
RN7. Dados enviados ao provedor de modelo não incluem e-mail, nome de colaborador nem metas individuais;
     colaboradores aparecem como papéis ("responsável", "gestor").
RN8. Trocar modelo ou prompt exige rodar o conjunto de avaliação e não piorar as métricas de referência.

## Fora do escopo
Treinamento ou ajuste fino de modelo; transcrição de áudio de reunião.

## Impacto em API e MCP
Rotas de sugestão; contrato MCP completo em `contracts/mcp-tools.json`.

## Pronto quando
No piloto, o time aprova ou descarta sugestões reais, a taxa de aceitação é medida e o conjunto de avaliação roda no `make check`.

## Questões em aberto
- [DECIDIR] Provedor de modelo inicial e onde os dados podem ser processados (política de dados da organização).
- [DECIDIR] Métrica de referência mínima para liberar (ex.: causa correta entre as 3 primeiras em X% dos casos do conjunto).

# F10 – Escala e migração

Status: Rascunho · Release: R3 · Depende de: F01 a F08 estáveis no piloto

## Objetivo
Levar o sistema do setor piloto para todas as frentes: entrada rápida de setores e pessoas, migração das planilhas
existentes, Gestão à Vista em TV e operação preparada para volume e LGPD.

## Perfis envolvidos
admin, escritorio, leitor, diretoria.

## Histórias
1. Como admin, quero sincronizar colaboradores e setores com o diretório corporativo (ou importar CSV).
2. Como escritório, quero importar indicadores, metas e histórico de medições de planilhas no formato atual
   (modelo "Indicadores Operacionais", uma aba por setor), com prévia e relatório de erros antes de gravar.
3. Como escritório, quero liberar um painel de Gestão à Vista para um perfil leitor exibido em TV, com rotação de telas.
4. Como diretoria, quero um painel consolidado de todos os setores (farol, situação SDCA, diagnóstico).
5. Como admin, quero exportar e anonimizar dados de um colaborador desligado (LGPD).

## Regras de negócio
RN1. Sincronização não apaga: colaborador ausente na origem vira desligado; setor ausente vira inativo.
RN2. Importação é em duas etapas: prévia (validação completa, nada gravado) e confirmação (transação única por arquivo).
RN3. Linha inválida não impede as outras na prévia, mas a confirmação só ocorre sem erros ou com as linhas inválidas excluídas
     explicitamente pelo usuário.
RN4. Medições importadas têm origem "importacao" e não disparam abertura automática de anomalia para períodos passados.
RN5. Painel de TV não mostra metas individuais nem nomes de pessoas; atualiza sozinho [SUPOSIÇÃO] a cada 5 minutos.
RN6. Anonimização substitui nome e e-mail por identificador, preservando histórico de indicadores e auditoria.
RN7. Metas de desempenho: listas e painéis respondem em até 2 s com 50 setores, 2.000 indicadores e 36 meses de histórico.
     [SUPOSIÇÃO] volume.

## Fora do escopo
Integrações com ERP e Microsoft 365 além de diretório (evoluções do padrão da F06).

## Impacto em API e MCP
Rotas de sincronização, importação (prévia/confirmação), painel TV, painel consolidado, LGPD.

## Pronto quando
Todas as frentes rodam sem planilha paralela por um ciclo completo de fechamento mensal.

## Questões em aberto
- [DECIDIR] Fonte de verdade de pessoas: Entra ID, sistema de RH ou CSV?
- [DECIDIR] Quanto histórico migrar das planilhas (assumido: ciclo atual e anterior).

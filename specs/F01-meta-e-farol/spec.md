# F01 – Meta e farol

Status: Rascunho · Release: R1 · Depende de: F00

## Objetivo
O escritório de gestão cadastra a estrutura (setores, colaboradores, tipos de indicador, ciclo, objetivos e indicadores
com meta) e o gestor acompanha o painel do setor com farol e histórico.

## Perfis envolvidos
admin, escritorio, gestor, colaborador.

## Histórias
1. Como escritório, quero cadastrar setores com setor pai e gestor, para refletir a estrutura da organização.
2. Como escritório, quero cadastrar colaboradores com setor, gestor e perfil.
3. Como escritório, quero cadastrar tipos de indicador com as 5 dimensões.
4. Como escritório, quero abrir um ciclo e cadastrar objetivos estratégicos por perspectiva.
5. Como escritório, quero cadastrar indicadores de setor com tipo, fórmula, unidade, periodicidade, responsável e meta.
6. Como gestor, quero ver o painel do meu setor com o farol de cada indicador e a série dos últimos 12 meses.

## Regras de negócio
RN1. Sigla de setor é única. Um setor não pode ser pai de si mesmo nem de um ancestral.
RN2. E-mail de colaborador é único; colaborador desligado não acessa o sistema.
RN3. Farol para as três polaridades: maior_melhor (RN4 da F00); menor_melhor: verde se valor ≤ meta,
     amarelo se ≤ meta × (1 + tolerância), vermelho caso contrário; faixa: verde se entre mínimo e máximo,
     amarelo se fora da faixa por até a tolerância (percentual sobre o limite violado), vermelho caso contrário.
RN4. Meta pode ser única para o ciclo ou por período; meta do período prevalece.
RN5. Indicador inativo não aparece no painel, mas mantém histórico.
RN6. Mudança de meta é auditada.
RN7. O gestor vê todos os indicadores do próprio setor e dos setores descendentes.

## Fora do escopo
Árvore pai/filho e consolidação (F02); aceite de meta (F02); importação em massa (F10).

## Impacto em API e MCP
CRUD de setor, colaborador, tipo_indicador, ciclo, objetivo, indicador, meta; `GET /paineis/setor/{id}`. Sem MCP.

## Pronto quando
Um setor real acompanha de 3 a 5 indicadores no sistema durante um fechamento mensal.

## Questões em aberto
- [DECIDIR] Quais perspectivas do mapa estratégico usar (padrão BSC: Clientes, Finanças, Processos, Pessoas)?
- [DECIDIR] Periodicidades além de mensal e trimestral são necessárias?

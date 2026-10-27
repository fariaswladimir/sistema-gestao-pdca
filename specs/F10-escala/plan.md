# F10 – Plano

## Componentes
- `integracoes/diretorio.py`: sincronização com Entra ID (Graph) ou CSV; job diário.
- `importacao/planilha_operacional.py`: leitor openpyxl para o modelo "uma aba por setor"; mapeamento de colunas
  (setor, colaborador, indicador, meta, fórmula, orientação, unidade); validação; prévia persistida em tabela temporária.
- Medição com origem `importacao` (novo valor de enum; migração) e regra de anomalia ignorando importação.
- Painel TV: rota pública por token de leitor, layout de tela cheia, rotação, sem dados pessoais.
- Painel consolidado: consultas agregadas com índices e visão materializada por período se necessário (registrar decisão).
- LGPD: exportação JSON dos dados da pessoa e anonimização transacional.
- Carga: script de geração de base sintética + teste de desempenho (k6 ou Locust) no CI noturno.

## Testes
Importação com planilhas de exemplo em `seed/planilhas/` (anonimizadas), sincronização simulada, LGPD, desempenho, aceitação, permissões.

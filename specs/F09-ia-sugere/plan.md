# F09 – Plano

## Modelo de dados
`sugestao_ia`, `documento_vetor` (pgvector; dimensão conforme o modelo de embedding escolhido; registrar em decisoes.md).

## Componentes
- `ia/gateway.py`: interface única (`completar`, `embutir`) com adaptadores por provedor; modelo e chave por configuração.
- `ia/anonimizar.py`: troca nomes e e-mails por papéis antes de enviar (RN7) e restaura na resposta.
- `ia/indexador.py`: indexa anomalias encerradas, lições, POPs vigentes e atas, com `setor_id` para filtro de escopo.
- `ia/sugestoes/causas.py`, `plano.py`, `ata.py`: recuperar evidências (filtradas por escopo) → montar prompt versionado
  (`ia/prompts/*.md` com versão) → validar saída em schema → gravar sugestão pendente.
- `mcp/ferramentas/`: ferramentas de escrita usando os serviços existentes com `escrita=True`.
- Telas: painel lateral "Sugestões da IA" na anomalia, no plano e no ritual, com evidências clicáveis, editar, aceitar, descartar, avaliar.

## Avaliação
- `tests/evals/causas/`: casos (anomalia + causa raiz real) montados a partir do seed; métrica: causa correta entre as 3 primeiras.
- `make evals` roda com o modelo configurado; no CI usa modelo simulado para testes e, em job separado, o real.
- Painel de qualidade: taxa de aceitação e nota média por tipo.

## Testes
Aceitação com modelo simulado, anonimização (nenhum dado pessoal na requisição), escopo das evidências, contrato MCP, permissões.

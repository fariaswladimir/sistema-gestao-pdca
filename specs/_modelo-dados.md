# Modelo de dados (canônico)

Toda tabela tem `id` (UUID v7), `criado_em`, `atualizado_em`. A fatia que cria cada tabela está entre parênteses.

## Organização e acesso
- **setor** (F01): nome, sigla, setor_pai_id, gestor_id, unidade, ativo, caminho (ltree)
- **colaborador** (F00/F01): nome, email (único), setor_id, cargo, gestor_id, perfil, status (ativo, afastado, desligado), sub_oidc
- **credencial_api** (F06): nome, client_id, segredo_hash, escopos[], setor_escopo_id, criado_por, expira_em, revogada_em

## Estratégia e desdobramento
- **ciclo** (F01): nome, inicio, fim, status (planejamento, vigente, encerrado)
- **objetivo** (F01): ciclo_id, perspectiva, codigo, titulo, visao_negocio, beneficio
- **tipo_indicador** (F01): nome, nivel (estrategico, setor, time, individual), natureza (controle, verificacao),
  polaridade (maior_melhor, menor_melhor, faixa), consolidacao (soma, media, media_ponderada, ultimo, nenhuma),
  origem (manual, integracao, calculado)
- **indicador** (F00/F01/F02): codigo, nome, tipo_id, objetivo_id, pai_id, peso (para media_ponderada), caminho (ltree),
  setor_id, responsavel_id, formula_descricao, unidade, periodicidade (mensal, trimestral), tolerancia_pct,
  publicado (bool), papel (F08: indice_execucao_gestao), ativo
- **meta** (F01): indicador_id, ciclo_id, periodo (null = meta do ciclo), valor, valor_min, valor_max
- **aceite_meta** (F02): meta_id, colaborador_id, aceito_em, gestor_id, gestor_aceito_em, status (pendente, aceita, contestada), comentario

## Medição
- **medicao** (F00): indicador_id, periodo (date, dia 1), valor, origem (manual, integracao, calculado; importacao na F10),
  registrado_por, farol (verde, amarelo, vermelho, sem_dado), justificativa_correcao
- **mapeamento_fonte** (F06): indicador_id, integracao_id, consulta (JQL ou expressão), transformacao, agendamento

## PDCA
- **anomalia** (F03): indicador_id, periodo, titulo, descricao, status (rascunho, em_analise, plano_definido,
  em_verificacao, eficaz, ineficaz, cancelada), origem (manual, regra, ia), setor_id, criado_por, aprovado_por
- **causa** (F03): anomalia_id, categoria (metodo, maquina, mao_de_obra, material, medida, meio_ambiente), descricao, raiz (bool), origem
- **plano_acao** (F03): anomalia_id, indicador_id, status (rascunho, aprovado, concluido, cancelado), aprovado_por
- **acao** (F03): plano_id, descricao, responsavel_id, prazo, status (aberta, em_andamento, concluida, cancelada), concluida_em, origem (manual, ritual, ia)
- **verificacao_eficacia** (F03): anomalia_id, periodo_verificado, resultado (eficaz, ineficaz), observacao, verificado_por
- **licao** (F04): anomalia_id, texto, tags[]

## SDCA
- **padrao** (F04): setor_id, indicador_id, titulo, tarefa_critica, conteudo (markdown), versao, status (rascunho, vigente, obsoleto),
  origem_anomalia_id, dono_id, periodicidade_dto
- **verificacao_dto** (F04): padrao_id, colaborador_id, data_prevista, data_realizada, aderente (bool), desvios, verificado_por

## Rituais
- **tipo_ritual** (F05): nome, cadencia (diaria, semanal, mensal, quadrimestral, semestral), regras_pauta (json)
- **ritual** (F05): tipo_id, setor_id, data_hora, pauta (json), ata (markdown), status (agendado, realizado, cancelado), conduzido_por
- **decisao** (F05): ritual_id, texto, acao_id (se virou ação)
- **presenca** (F05): ritual_id, colaborador_id, presente

## Diagnóstico
- **item_diagnostico** (F08): codigo, criterio, tipo (automatico, manual), regra (identificador da regra), peso, evidencia_esperada, ativo
- **diagnostico** (F08): setor_id, periodo_inicio, periodo_fim, nota, status (aberto, fechado), fechado_por
- **resultado_item** (F08): diagnostico_id, item_id, nota (0 a 100), evidencias (json), avaliado_por, origem (regra, humano)

## IA, integração e auditoria
- **sugestao_ia** (F09): tipo (causas, plano, ata, pauta), alvo_tipo, alvo_id, conteudo (json), evidencias (json),
  modelo, versao_prompt, status (pendente, aceita, aceita_editada, descartada), decidido_por, avaliacao (1 a 5)
- **documento_vetor** (F09): fonte_tipo (anomalia, licao, padrao, ata), fonte_id, setor_id, trecho, embedding (vector)
- **integracao** (F06): tipo (jira, m365, planilha), nome, config (json), segredo_ref, ativa
- **webhook_assinatura** (F06): url, eventos[], segredo_hash, ativa, criado_por
- **webhook_entrega** (F06): assinatura_id, evento, payload, tentativas, status, proxima_tentativa
- **fila_tarefa** (F00): tipo, payload, status, tentativas, executar_em
- **evento_auditoria** (F00): entidade, entidade_id, acao, antes (json), depois (json), ator_id, ator_tipo (humano, servico, ia),
  modelo_ia, canal (web, api, mcp), em

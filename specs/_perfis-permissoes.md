# Perfis e permissões

## Perfis
| Perfil | Quem é |
| --- | --- |
| admin | TI / dono técnico do sistema |
| escritorio | Escritório de gestão (cuida do método; na FIEPE, o NGTI) |
| diretoria | Alta gestão |
| gestor | Líder de setor ou time |
| colaborador | Membro de um setor |
| leitor | Painel de TV, convidado, auditor externo |
| servico | Conta técnica de integração ou agente de IA |

## Escopo
- colaborador e gestor: o próprio setor e descendentes, mais indicadores estratégicos publicados.
- diretoria, escritorio, admin: toda a organização.
- leitor: apenas painéis liberados a ele.
- servico: escopo definido na credencial; nunca maior que o do usuário que a criou.
- Metas individuais: só o próprio colaborador, o gestor do setor, escritorio e admin.
- Recurso fora do escopo responde 404 (não revelar existência).

## Matriz (✔ permitido · ✖ negado · R rascunho)
| Ação | admin | escritorio | diretoria | gestor | colaborador | leitor | servico |
| --- | --- | --- | --- | --- | --- | --- | --- |
| setor:gerir | ✔ | ✔ | ✖ | ✖ | ✖ | ✖ | ✖ |
| colaborador:gerir | ✔ | ✔ | ✖ | ✖ | ✖ | ✖ | ✖ |
| tipo_indicador:gerir | ✖ | ✔ | ✖ | ✖ | ✖ | ✖ | ✖ |
| objetivo:gerir | ✖ | ✔ | ✔ | ✖ | ✖ | ✖ | ✖ |
| indicador:criar_estrategico | ✖ | ✔ | ✔ | ✖ | ✖ | ✖ | ✖ |
| indicador:desdobrar | ✖ | ✔ | ✔ | ✔ | ✖ | ✖ | ✖ |
| indicador:ler | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| meta:aceitar | ✖ | ✖ | ✔ | ✔ | ✔ | ✖ | ✖ |
| medicao:registrar | ✖ | ✔ | ✖ | ✔ | ✔ | ✖ | ✔ |
| anomalia:criar | ✖ | ✔ | ✖ | ✔ | ✔ | ✖ | R |
| anomalia:editar | ✖ | ✔ | ✖ | ✔ | ✔ | ✖ | R |
| anomalia:aprovar | ✖ | ✔ | ✖ | ✔ | ✖ | ✖ | ✖ |
| plano:gerir | ✖ | ✔ | ✖ | ✔ | ✖ | ✖ | R |
| acao:atualizar | ✖ | ✔ | ✖ | ✔ | ✔ (próprias) | ✖ | ✖ |
| padrao:gerir | ✖ | ✔ | ✖ | ✔ | ✖ | ✖ | R |
| dto:registrar | ✖ | ✔ | ✖ | ✔ | ✖ | ✖ | ✖ |
| ritual:conduzir | ✖ | ✔ | ✔ | ✔ | ✖ | ✖ | R |
| diagnostico:avaliar | ✖ | ✔ | ✖ | ✖ | ✖ | ✖ | ✖ |
| diagnostico:ler | ✔ | ✔ | ✔ | ✔ | ✔ | ✖ | ✔ |
| integracao:gerir | ✔ | ✖ | ✖ | ✖ | ✖ | ✖ | ✖ |
| credencial_api:gerir | ✔ | ✖ | ✖ | ✖ | ✖ | ✖ | ✖ |
| auditoria:ler | ✔ | ✔ | ✔ | ✖ | ✖ | ✖ | ✖ |
| painel:ler | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

A matriz executável fica em `tests/permissions/matriz.yaml` e deve espelhar esta tabela.

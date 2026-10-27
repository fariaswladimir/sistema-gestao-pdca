# F00 – Plano

## Modelo de dados e migrações
- Extensões `ltree`, `vector` (criadas já, usadas depois).
- Tabelas mínimas: `setor` (nome, sigla), `colaborador` (nome, email, setor_id, perfil, sub_oidc),
  `tipo_indicador`, `indicador` (campos básicos), `meta`, `medicao`, `evento_auditoria`, `fila_tarefa`.
- Seed: 1 setor, 2 colaboradores, 1 tipo maior_melhor, 2 indicadores com meta.

## Regras de domínio e motor
- `motor/farol.py`: função pura `calcular_farol(valor, meta, polaridade, tolerancia)`; nesta fatia só maior_melhor ativo,
  mas a assinatura já recebe polaridade.
- `seguranca/permissoes.py`: esqueleto de `exigir_permissao` e `escopo` (nesta fatia: responsável = usuário).
- `auditoria.py`: `registrar_auditoria(...)`.

## Eventos
`MedicaoRegistrada` publicado (sem consumidores ainda).

## API
| Método | Rota | Permissão |
| --- | --- | --- |
| GET | /saude | pública |
| GET | /auth/login, /auth/callback, POST /auth/logout | pública |
| GET | /eu | autenticado |
| GET | /indicadores/meus | indicador:ler |
| GET | /indicadores/{id} | indicador:ler |
| PUT | /indicadores/{id}/medicoes/{periodo} | medicao:registrar |

## Telas
- Login (redireciona ao Keycloak em dev).
- "Meus indicadores": cartão com nome, meta, último valor, farol (ícone + texto + cor), formulário de lançamento.

## Infra
- `docker-compose.yml`: postgres 16 (com pgvector), keycloak com realm de dev, api, web.
- GitHub Actions: lint, typecheck, testes, build de imagens, deploy em homologação.
- Logs estruturados JSON; `/saude` com versão e checagem de banco.

## Testes por camada
- Unitário: tabela de casos do farol.
- Aceitação: `acceptance.feature`.
- Permissões: matriz inicial com indicador:ler e medicao:registrar.
- E2E: login → lançar → ver farol.

## Riscos
- Configuração de OIDC consumir a fatia inteira: usar Keycloak local com realm exportado no repositório.

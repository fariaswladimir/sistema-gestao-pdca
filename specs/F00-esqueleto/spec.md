# F00 – Esqueleto andante

Status: Aprovada (ajustada em 2026-10-28 pelas diretrizes de versão do AGENTS.md) · Release: R0 · Depende de: nenhuma

## Objetivo
Provar que o sistema funciona de ponta a ponta, primeiro na máquina local: um colaborador entra, lança o valor de um indicador
e vê o farol. Tudo o que vier depois cresce sobre este esqueleto.

## Perfis envolvidos
colaborador (único perfil ativo nesta fatia; os demais existem só no cadastro).

## Histórias
1. Como colaborador, quero entrar escolhendo meu usuário numa lista (modo local, sem senha) para usar o sistema.
   O login com senha (Keycloak) já existe e é religado por configuração na fatia de autenticação.
2. Como colaborador, quero ver o indicador sob minha responsabilidade com meta e farol do mês.
3. Como colaborador, quero lançar o valor do mês e ver o farol recalculado na hora.

## Regras de negócio
RN1. Sem usuário na sessão (escolhido no modo local ou autenticado no modo oidc), nenhuma tela ou rota de dados
     é acessível (exceto `/saude` e, no modo local, a lista de usuários para escolha).
RN2. "Meus indicadores" lista os indicadores dos quais o colaborador é responsável. Restrição de acesso por perfil
     e setor só nas versões finais; até lá, qualquer usuário abre e lança em qualquer indicador.
RN3. Uma medição por indicador e período; lançar de novo o mesmo período substitui o valor e exige justificativa.
RN4. Farol para polaridade maior_melhor: verde se valor ≥ meta; amarelo se valor ≥ meta × (1 − tolerância);
     vermelho caso contrário; sem_dado se não há medição. Tolerância padrão 5%.
RN5. Toda medição gera evento de auditoria com antes e depois.

## Fora do escopo
Cadastros pela interface (F01), outras polaridades e árvore (F01/F02), anomalias (F03).
Login com conta corporativa (SSO) fica para versão futura. Perfis e escopo de acesso: versões finais (F09/F10).
Indicador, setor e colaborador desta fatia vêm do seed.

## Impacto em API e MCP
Rotas de sessão, `GET /indicadores/meus`, `GET /indicadores/{id}`, `PUT /indicadores/{id}/medicoes/{periodo}`, `GET /saude`.
Sem MCP.

## Pronto quando
Roda com `make up` na máquina local, sem Keycloak, com dados de exemplo, e os cenários de aceite estão verdes no pipeline.
A homologação em servidor interno (deploy automático, monitoramento) está pronta em código e adiada até haver servidor.

## Questões em aberto
Nenhuma. Decididas em 2026-10-27 (ver `decisoes.md`): login e senha próprios do sistema na v1;
homologação e produção em servidor interno; tolerância padrão de 5%.

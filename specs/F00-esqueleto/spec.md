# F00 – Esqueleto andante

Status: Aprovada · Release: R0 · Depende de: nenhuma

## Objetivo
Provar que o sistema funciona de ponta a ponta em produção: um colaborador entra, lança o valor de um indicador
e vê o farol. Tudo o que vier depois cresce sobre este esqueleto.

## Perfis envolvidos
colaborador (único perfil ativo nesta fatia; os demais existem só no cadastro).

## Histórias
1. Como colaborador, quero entrar com meu login e senha do sistema para usá-lo com segurança.
2. Como colaborador, quero ver o indicador sob minha responsabilidade com meta e farol do mês.
3. Como colaborador, quero lançar o valor do mês e ver o farol recalculado na hora.

## Regras de negócio
RN1. Sem autenticação, nenhuma tela ou rota de dados é acessível (exceto `/saude`).
RN2. O colaborador só vê indicadores dos quais é responsável (escopo mínimo desta fatia).
RN3. Uma medição por indicador e período; lançar de novo o mesmo período substitui o valor e exige justificativa.
RN4. Farol para polaridade maior_melhor: verde se valor ≥ meta; amarelo se valor ≥ meta × (1 − tolerância);
     vermelho caso contrário; sem_dado se não há medição. Tolerância padrão 5%.
RN5. Toda medição gera evento de auditoria com antes e depois.

## Fora do escopo
Cadastros pela interface (F01), outras polaridades e árvore (F01/F02), anomalias (F03).
Login com conta corporativa (SSO) fica para versão futura.
Indicador, setor e colaborador desta fatia vêm do seed.

## Impacto em API e MCP
Rotas de sessão, `GET /indicadores/meus`, `GET /indicadores/{id}`, `PUT /indicadores/{id}/medicoes/{periodo}`, `GET /saude`.
Sem MCP.

## Pronto quando
Está em um ambiente de homologação acessível (servidor interno), com deploy automático a cada merge na branch principal,
monitoramento básico (saúde, erros) e os cenários de aceite verdes no pipeline.

## Questões em aberto
Nenhuma. Decididas em 2026-10-27 (ver `decisoes.md`): login e senha próprios do sistema na v1;
homologação e produção em servidor interno; tolerância padrão de 5%.

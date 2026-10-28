# language: pt
Funcionalidade: Esqueleto andante

  Contexto:
    Dado o setor "Piloto" com o colaborador "ana" responsável pelo indicador "IND-01"
    E o indicador "IND-01" é "maior_melhor" com meta 80 e tolerância 5%

  Cenário: acesso sem usuário na sessão é negado
    Quando um visitante sem sessão acessa a lista de indicadores
    Então recebe resposta 401

  Cenário: verificação de saúde é pública
    Quando um visitante consulta a saúde do sistema
    Então recebe resposta 200 com status "ok" e versão

  Cenário: colaborador vê seu indicador sem dado
    Dado "ana" está autenticada
    Quando ela consulta seus indicadores
    Então vê "IND-01" com farol "sem_dado" no período atual

  Esquema do Cenário: farol calculado ao lançar a medição
    Dado "ana" está autenticada
    Quando ela lança o valor <valor> em "IND-01" no período "2026-10"
    Então o farol de "IND-01" em "2026-10" é "<farol>"

    Exemplos:
      | valor | farol    |
      | 85    | verde    |
      | 80    | verde    |
      | 77    | amarelo  |
      | 76    | amarelo  |
      | 75.9  | vermelho |

  Cenário: relançar o mesmo período exige justificativa
    Dado "ana" lançou 70 em "IND-01" no período "2026-10"
    Quando ela lança 82 no mesmo período sem justificativa
    Então recebe resposta 422
    Quando ela lança 82 no mesmo período com justificativa "erro de digitação"
    Então o farol passa a "verde"
    E existe evento de auditoria da medição com valor anterior 70 e novo 82

  Cenário: a lista mostra só os indicadores de que a colaboradora é responsável
    Dado o indicador "IND-02" sob responsabilidade de "bruno"
    E "ana" está autenticada
    Quando ela consulta seus indicadores
    Então vê "IND-01" e não vê "IND-02"

  Cenário: no modo local, a entrada lista os colaboradores ativos para escolha
    Quando um visitante abre a escolha de usuário
    Então vê "Ana" na lista, sem e-mail

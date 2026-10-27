# language: pt
Funcionalidade: Meta e farol

  Cenário: escritório cadastra setor com setor pai
    Dado "eva" com perfil escritorio está autenticada
    Quando ela cadastra o setor "NGTI" com pai "Sede" e gestor "carlos"
    Então o setor "NGTI" aparece como filho de "Sede"

  Cenário: hierarquia circular é rejeitada
    Dado os setores "Sede" e "NGTI" filho de "Sede"
    Quando "eva" define "NGTI" como pai de "Sede"
    Então recebe resposta 422 com a mensagem "hierarquia circular"

  Esquema do Cenário: farol por polaridade
    Dado um indicador "<polaridade>" com meta <meta>, mínimo <min>, máximo <max> e tolerância 5%
    Quando é lançado o valor <valor>
    Então o farol é "<farol>"

    Exemplos:
      | polaridade   | meta | min | max | valor | farol    |
      | menor_melhor | 10   |     |     | 9     | verde    |
      | menor_melhor | 10   |     |     | 10.4  | amarelo  |
      | menor_melhor | 10   |     |     | 11    | vermelho |
      | faixa        |      | 90  | 110 | 100   | verde    |
      | faixa        |      | 90  | 110 | 88    | amarelo  |
      | faixa        |      | 90  | 110 | 80    | vermelho |

  Cenário: meta do período prevalece sobre a do ciclo
    Dado o indicador "IND-03" com meta de ciclo 80 e meta de "2026-12" igual a 90
    Quando é lançado 86 em "2026-12"
    Então o farol de "2026-12" é "amarelo"

  Cenário: gestor vê painel do setor e dos descendentes
    Dado "carlos" é gestor de "Sede", que tem o filho "NGTI"
    E existem indicadores ativos em "Sede" e em "NGTI"
    Quando "carlos" abre o painel de "Sede"
    Então vê os indicadores dos dois setores com farol e série de 12 meses

  Cenário: colaborador não cadastra indicador
    Dado "ana" com perfil colaborador está autenticada
    Quando ela tenta cadastrar um indicador
    Então recebe resposta 403

  Cenário: mudança de meta é auditada
    Quando "eva" altera a meta do ciclo de "IND-03" de 80 para 85
    Então existe evento de auditoria com valor anterior 80 e novo 85 e ator "eva"

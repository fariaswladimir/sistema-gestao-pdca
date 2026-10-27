# language: pt
Funcionalidade: Escala e migração

  Cenário: sincronização não apaga colaborador
    Dado "joao" ativo no sistema e ausente no diretório
    Quando a sincronização roda
    Então "joao" fica "desligado" e seu histórico permanece

  Cenário: prévia de importação não grava
    Dado a planilha "Indicadores_Operacionais_2027.xlsx" com 3 abas de setor e 2 linhas inválidas
    Quando "eva" envia para prévia
    Então recebe o relatório com 2 erros indicando aba, linha e motivo
    E nada é gravado

  Cenário: confirmação excluindo linhas inválidas
    Dado a prévia com 2 linhas inválidas
    Quando "eva" confirma excluindo as linhas inválidas
    Então os indicadores válidos são criados em uma única transação

  Cenário: histórico importado não abre anomalia
    Dado medição importada vermelha em "2026-03"
    Então não existe anomalia aberta por regra para "2026-03"

  Cenário: painel de TV sem dados pessoais
    Dado o leitor "tv-sala-1" com o painel do setor "Piloto"
    Quando o painel é exibido
    Então mostra farol e situação SDCA dos indicadores do setor
    E não mostra metas individuais nem nomes de pessoas

  Cenário: anonimização LGPD
    Dado "joao" desligado
    Quando "root" anonimiza "joao"
    Então nome e e-mail de "joao" são substituídos por identificador
    E as medições e eventos de auditoria permanecem ligados ao identificador

  Cenário: desempenho do painel consolidado
    Dado a base de carga com 50 setores, 2000 indicadores e 36 meses
    Quando a diretoria abre o painel consolidado
    Então a resposta chega em até 2 segundos

# language: pt
Funcionalidade: Diagnóstico da gestão

  Contexto:
    Dado o diagnóstico do setor "Piloto" de "2026-09" a "2026-12" aberto
    E os itens automáticos A1 a A6 com peso 1

  Cenário: A1 penaliza vermelho sem anomalia
    Dado 4 indicadores vermelhos no período, 3 com anomalia aberta no mesmo mês
    Então a nota parcial do item A1 é 75
    E as evidências listam o indicador sem anomalia

  Cenário: item sem base é não aplicável
    Dado nenhum indicador vermelho no período
    Então o item A1 vale 100 com a marca "não aplicável no período"

  Cenário: A3 conta lançamentos até o dia 5
    Dado 10 medições do período, 8 registradas até o dia 5 do mês seguinte
    Então a nota do item A3 é 80

  Cenário: item manual exige comentário
    Dado o item manual M1
    Quando "eva" do escritório avalia M1 com nota 70 sem comentário
    Então recebe resposta 422

  Cenário: fechamento alimenta o indicador estratégico
    Dado os setores "Piloto" com nota 80 e "Outro" com nota 60 e pesos iguais
    Quando "eva" fecha os diagnósticos do período
    Então o indicador "Índice de execução da gestão" recebe 70 no período de fechamento

  Cenário: diagnóstico fechado é imutável
    Dado o diagnóstico fechado
    Quando "eva" tenta alterar a nota de M1
    Então recebe resposta 409

  Cenário: gestor não avalia
    Quando "carlos" tenta avaliar o item M1
    Então recebe resposta 403

  Cenário: consulta via MCP
    Dado "carlos" conectado via MCP
    Quando ele chama "consultar_diagnostico" para o setor "Piloto"
    Então recebe a nota parcial e os itens com pior nota primeiro

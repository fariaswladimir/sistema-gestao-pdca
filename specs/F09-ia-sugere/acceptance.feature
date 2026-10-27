# language: pt
Funcionalidade: IA sugere

  Contexto:
    Dado o modelo de IA simulado com respostas determinísticas
    E 5 anomalias encerradas no setor "Piloto" parecidas com a anomalia "A-02"

  Cenário: sugestão de causas cita evidências
    Dado "ana" analisando "A-02"
    Quando ela pede sugestão de causas
    Então recebe até 5 causas com categoria 6M
    E cada causa cita ao menos uma anomalia ou lição usada como evidência
    E a sugestão fica "pendente"

  Cenário: evidência insuficiente
    Dado nenhuma anomalia parecida visível para "ana"
    Quando ela pede sugestão de causas
    Então a resposta informa evidência insuficiente e não lista causas

  Cenário: escopo nas evidências
    Dado anomalias parecidas apenas no setor "Outro"
    Quando "ana" do setor "Piloto" pede sugestão
    Então nenhuma evidência do setor "Outro" é usada

  Cenário: aceitar com edição cria causa de origem IA
    Dado a sugestão pendente com a causa "roteiro desatualizado"
    Quando "ana" edita para "roteiro desatualizado no turno B" e aceita
    Então a anomalia "A-02" tem a causa editada com origem "ia"
    E a sugestão fica "aceita_editada"

  Cenário: plano via MCP nasce rascunho
    Dado "carlos" conectado via MCP
    Quando ele chama "criar_plano_acao" para "A-02"
    Então existe plano "rascunho" com origem "ia"
    E nenhuma ação está aprovada

  Cenário: MCP não aprova nem encerra
    Quando o cliente MCP lista as ferramentas
    Então nenhuma ferramenta aprova, encerra, exclui ou altera meta

  Cenário: dados pessoais não vão ao provedor
    Quando "ana" pede sugestão de causas
    Então a requisição enviada ao provedor não contém e-mails nem nomes de colaboradores

  Cenário: escrita via MCP é auditada como IA
    Quando "carlos" chama "abrir_anomalia" via MCP
    Então existe evento de auditoria com ator "carlos", tipo de ator "ia", canal "mcp" e modelo informado

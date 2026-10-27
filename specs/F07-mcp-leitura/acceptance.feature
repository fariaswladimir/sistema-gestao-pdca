# language: pt
Funcionalidade: MCP de leitura

  Cenário: sem token não há acesso
    Quando um cliente MCP sem token lista as ferramentas
    Então recebe erro de autenticação

  Cenário: catálogo de ferramentas de leitura
    Dado "ana" conectada via MCP
    Quando o cliente lista as ferramentas
    Então vê "consultar_arvore", "consultar_indicador", "listar_pendencias" e "consultar_padroes"
    E nenhuma ferramenta de escrita

  Cenário: consultar indicador respeita escopo
    Dado "ana" do setor "Piloto" conectada via MCP
    Quando ela chama "consultar_indicador" para um indicador do setor "Outro"
    Então recebe erro "não encontrado"

  Cenário: meta individual de colega não aparece
    Dado "bruno" do mesmo setor conectado via MCP
    Quando ele chama "consultar_arvore" do setor "Piloto"
    Então a resposta não contém indicadores individuais de "ana"

  Cenário: pendências do usuário
    Dado "ana" com 2 ações abertas, 1 vencida e 1 meta pendente de aceite
    Quando ela chama "listar_pendencias"
    Então a resposta lista as 3 ações e a meta, com a vencida destacada

  Cenário: acesso auditado
    Quando "ana" chama "consultar_indicador"
    Então existe evento de auditoria com canal "mcp", ferramenta "consultar_indicador" e cliente declarado

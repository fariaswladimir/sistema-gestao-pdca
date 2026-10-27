# language: pt
Funcionalidade: API pública, webhooks e Jira

  Cenário: segredo da credencial aparece uma vez
    Dado "root" com perfil admin
    Quando ele cria a credencial "bi-relatorios" com escopo "indicador:ler" no setor "Sede"
    Então a resposta contém o segredo
    E consultas seguintes da credencial não exibem o segredo

  Cenário: credencial respeita escopo
    Dado a credencial "bi-relatorios" com escopo "indicador:ler"
    Quando ela tenta registrar uma medição
    Então recebe resposta 403

  Cenário: coleta do Jira gera medição e dispara regras
    Dado o indicador "IND-20" maior_melhor meta 90 mapeado para percentual entre as JQL "A" e "B"
    E o Jira retorna 45 itens para "A" e 50 para "B"
    Quando a coleta de "2026-10" roda
    Então "IND-20" tem medição 90 em "2026-10" com origem "integracao"

  Cenário: falha na coleta preserva valor anterior
    Dado "IND-20" com medição 90 em "2026-10"
    E o Jira está indisponível
    Quando a coleta de "2026-10" roda
    Então "IND-20" continua com 90 em "2026-10"
    E o escritório recebe aviso de falha na integração

  Cenário: lançamento manual bloqueado em indicador integrado
    Quando "ana" tenta lançar valor em "IND-20"
    Então recebe resposta 409

  Cenário: webhook assinado de farol vermelho
    Dado uma assinatura de webhook para "farol.vermelho"
    Quando "IND-10" fica vermelho
    Então o destino recebe o evento com cabeçalho "X-Assinatura" válido
    E o payload não contém e-mail nem meta individual

  Cenário: webhook com falha é retentado
    Dado o destino responde 500
    Quando o evento é entregue
    Então há nova tentativa com espera crescente até 5 tentativas

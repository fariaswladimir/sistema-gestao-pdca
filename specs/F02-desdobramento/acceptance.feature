# language: pt
Funcionalidade: Desdobramento e aceite

  Contexto:
    Dado o objetivo "03 Fortalecer o modelo de gestão"
    E o indicador estratégico "E-3.2" com consolidação "media_ponderada", publicado

  Cenário: gestor desdobra indicador em filhos com peso
    Dado "carlos" é gestor de "Sede"
    Quando ele cria os filhos "S-NGTI" peso 2 e "S-NUCOM" peso 1 sob "E-3.2"
    Então a árvore de "E-3.2" mostra os dois filhos

  Cenário: consolidação ponderada
    Dado "S-NGTI" peso 2 com valor 90 e "S-NUCOM" peso 1 com valor 60 em "2026-10"
    Então o valor de "E-3.2" em "2026-10" é 80

  Cenário: pai sem dado enquanto falta filho
    Dado "S-NGTI" com valor 90 e "S-NUCOM" sem medição em "2026-10"
    Então "E-3.2" em "2026-10" está "sem_dado" com 1 filho pendente

  Cenário: correção do filho recalcula ancestrais
    Dado "E-3.2" consolidado em 80 em "2026-10"
    Quando o valor de "S-NUCOM" em "2026-10" é corrigido para 90 com justificativa
    Então o valor de "E-3.2" em "2026-10" é 90

  Cenário: pai consolidado não aceita lançamento manual
    Quando "carlos" tenta lançar valor em "E-3.2"
    Então recebe resposta 409

  Cenário: filho com nível superior ao pai é rejeitado
    Dado o indicador de time "T-01"
    Quando "carlos" tenta criar um filho estratégico sob "T-01"
    Então recebe resposta 422

  Cenário: aceite de meta individual
    Dado a meta individual de "ana" em "I-ANA-01" com status "pendente"
    Quando "ana" aceita a meta
    E "carlos" aceita a meta
    Então a meta fica "aceita"

  Cenário: contestação exige comentário
    Quando "ana" contesta a meta sem comentário
    Então recebe resposta 422

  Cenário: meta individual é privada
    Dado "bruno" colaborador do mesmo setor de "ana"
    Quando "bruno" consulta "I-ANA-01"
    Então recebe resposta 404

  Cenário: estratégico publicado é visível a todos
    Dado "bruno" colaborador de outro setor
    Quando ele consulta a árvore do objetivo "03"
    Então vê "E-3.2" com farol, mas não vê os indicadores individuais

"""Vocabulário do domínio (valores gravados no banco e expostos na API)."""

from enum import StrEnum


class Perfil(StrEnum):
    admin = "admin"
    escritorio = "escritorio"
    diretoria = "diretoria"
    gestor = "gestor"
    colaborador = "colaborador"
    leitor = "leitor"
    servico = "servico"


class StatusColaborador(StrEnum):
    ativo = "ativo"
    afastado = "afastado"
    desligado = "desligado"


class StatusCiclo(StrEnum):
    planejamento = "planejamento"
    vigente = "vigente"
    encerrado = "encerrado"


class Nivel(StrEnum):
    estrategico = "estrategico"
    setor = "setor"
    time = "time"
    individual = "individual"


class Natureza(StrEnum):
    controle = "controle"
    verificacao = "verificacao"


class Polaridade(StrEnum):
    maior_melhor = "maior_melhor"
    menor_melhor = "menor_melhor"
    faixa = "faixa"


class Consolidacao(StrEnum):
    soma = "soma"
    media = "media"
    media_ponderada = "media_ponderada"
    ultimo = "ultimo"
    nenhuma = "nenhuma"


class Origem(StrEnum):
    manual = "manual"
    integracao = "integracao"
    calculado = "calculado"


class Periodicidade(StrEnum):
    mensal = "mensal"
    trimestral = "trimestral"


class Farol(StrEnum):
    verde = "verde"
    amarelo = "amarelo"
    vermelho = "vermelho"
    sem_dado = "sem_dado"


class AtorTipo(StrEnum):
    humano = "humano"
    servico = "servico"
    ia = "ia"


class Canal(StrEnum):
    web = "web"
    api = "api"
    mcp = "mcp"


class StatusTarefa(StrEnum):
    pendente = "pendente"
    em_execucao = "em_execucao"
    concluida = "concluida"
    falhou = "falhou"

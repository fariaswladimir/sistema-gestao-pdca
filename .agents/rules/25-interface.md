---
trigger: always_on
---

# Interface (referência: Atlassian Design System)

O dono do produto escolheu o [Atlassian Design System](https://atlassian.design/design-system) (ADS) como
referência de interface em 2026-10-28. Seguimos o **método** do ADS, com implementação nossa.

## Por que referência e não dependência
A licença do ADS só permite usar o código, os ativos visuais e os pacotes em extensões que funcionam com
produtos Atlassian. Este sistema é independente. Portanto:
- **não** instale pacotes `@atlaskit/*` nem `@atlassian/*`;
- **não** use a fonte Atlassian Sans, os ícones, as ilustrações nem os logotipos da Atlassian;
- **não** copie código-fonte de componentes do ADS. Estudar a documentação (uso, anatomia, conteúdo,
  acessibilidade) e aplicar os mesmos princípios é o que fazemos.

## Tokens (frontend/app/globals.css)
- Cor só por token semântico, nunca cor crua (`slate-600`, `#fff`, `red-700`) em componente.
  Nome no padrão do ADS, em português: papel + propriedade + ênfase.
  - Texto: `text-texto`, `text-texto-sutil`, `text-texto-mais-sutil`, `text-texto-inverso`, `text-link`.
  - Fundo e superfície: `bg-fundo-pagina`, `bg-superficie`, `bg-superficie-elevada`, `bg-fundo-neutro`,
    `bg-fundo-marca`, `bg-fundo-selecionado` (com `-hover` quando houver).
  - Borda: `border-borda`, `border-borda-forte`, `border-borda-foco`.
  - Papéis semânticos `sucesso`, `alerta`, `perigo`, `info`, `neutro`, cada um com `-fundo`, `-texto`, `-borda`.
  - Elevação: `shadow-elevada` (cartão), `shadow-sobreposta` (menu, diálogo).
- Token novo entra em `globals.css` nos dois temas (claro e escuro); nunca só em um.
- Espaço na grade de 8 px (meio passo de 4 px): use a escala do Tailwind (`gap-2` = 8 px, `p-4` = 16 px).
- Tipografia: `text-corpo` (14/20, padrão do `body`), `text-corpo-pequeno` (rótulos, lozenges),
  `text-titulo-pequeno`, `text-titulo-medio`, `text-titulo-grande`. Pesos: normal, `font-semibold`.
- Raio: `rounded` (4 px) em botão, campo e lozenge; `rounded-lg` (8 px) em cartão.

## Componentes base (frontend/components/ui/)
Use-os antes de escrever HTML estilizado à mão; crie um novo aqui quando o padrão se repetir.

| Nosso | Equivalente ADS | Uso |
| --- | --- | --- |
| `Botao` (`primaria`, `padrao`, `sutil`, `perigo`) | Button | Uma ação primária por tela ou cartão. |
| `Etiqueta` (`sucesso`, `alerta`, `perigo`, `info`, `neutro`) | Lozenge | Status curto, não interativo, em caixa de frase. |
| `MensagemSecao` | Section message | Aviso em bloco com ícone e título. |
| `Campo` | Text field | Rótulo acima, ajuda abaixo, foco visível. |

Componentes de domínio (`components/dominio/`) compõem os base. Exemplo: `Farol` é uma `Etiqueta` semântica.

## Conteúdo e acessibilidade (do guia de escrita do ADS)
- Caixa de frase em tudo: títulos, botões, lozenges ("Fora do alvo", não "FORA DO ALVO" nem "Fora Do Alvo").
- Botão diz a ação com verbo ("Lançar", "Aprovar plano"); mensagem de erro diz o que fazer.
- Status nunca só por cor: texto claro e, quando ajudar, ícone (vale para o farol).
- Foco sempre visível (`CLASSE_FOCO`); alvos clicáveis com no mínimo 32 px de altura.
- Erro de formulário com `role="alert"`; confirmação com `aria-live="polite"`.

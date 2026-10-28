"""Gera docs/eap.html: a EAP (fatias e tarefas) e a etapa da fatia em andamento.

Fontes, todas em specs/: a tabela de fatias e a seção "Em andamento" do README.md e as caixas de cada
Fxx-*/tasks.md. Só biblioteca padrão. Uso: `make eap` (ou `python scripts/eap.py`).
"""

import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SPECS = RAIZ / "specs"
SAIDA = RAIZ / "docs" / "eap.html"

ETAPAS = ["Spec", "Plano", "Implementação", "Verificação", "Demo"]
GATES = [
    ("G1", "Esqueleto no ar", "F00"),
    ("G2", "PDCA rodando em 1 setor piloto", "F03"),
    ("G3", "Rotina sem planilha", "F06"),
]
STATUS_ORDEM = ["Rascunho", "Aprovada", "Em implementação", "Verificada", "Demonstrada"]


@dataclass
class Tarefa:
    codigo: str
    titulo: str
    feita: bool
    adiada: bool


@dataclass
class Fatia:
    codigo: str
    release: str
    nome: str
    status: str
    tarefas: list[Tarefa] = field(default_factory=list)

    @property
    def feitas(self) -> int:
        return sum(t.feita for t in self.tarefas)

    @property
    def pct(self) -> int:
        return round(100 * self.feitas / len(self.tarefas)) if self.tarefas else 0

    def etapa(self) -> int:
        """Etapa inferida (1–5; 6 = concluída) para fatias que não são a em andamento."""
        if self.status == "Demonstrada":
            return 6
        if self.status == "Verificada":
            return 5
        if self.status == "Rascunho":
            return 1
        return 3 if self.feitas else 2


def _fatias() -> list[Fatia]:
    readme = (SPECS / "README.md").read_text("utf-8")
    fatias = []
    for codigo, release, nome, status in re.findall(
        r"^\| (F\d\d) \| ([^|]+?) \| ([^|]+?) \| ([^|]+?) \|$", readme, re.M
    ):
        fatia = Fatia(codigo, release, nome, status)
        for tarefas in SPECS.glob(f"{codigo}-*/tasks.md"):
            texto = tarefas.read_text("utf-8")
            for marca, cod, resto in re.findall(r"^- \[([ x])\] (T\d+) (.*)$", texto, re.M):
                titulo = re.sub(r"\s*\(ADIADA[^)]*\)\s*", " ", resto).strip()
                titulo = titulo.split(". ")[0].rstrip(".")
                fatia.tarefas.append(Tarefa(cod, titulo, marca == "x", "(ADIADA" in resto))
        fatias.append(fatia)
    return fatias


def _em_andamento() -> dict[str, str]:
    readme = (SPECS / "README.md").read_text("utf-8")
    secao = readme.split("## Em andamento", 1)[1].split("\n## ", 1)[0]
    return dict(re.findall(r"^- ([^:]+): (.*)$", secao, re.M))


def _git(*args: str) -> str:
    try:
        saida = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, check=True)
        return saida.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "?"


def _gate(fatias: dict[str, Fatia], desde: str, ate: str) -> tuple[str, str]:
    """Atingido quando todas as fatias até ele estão demonstradas; em andamento se o trecho dele começou."""
    if all(f.status == "Demonstrada" for c, f in fatias.items() if c <= ate):
        return "feito", "Atingido"
    if any(f.feitas for c, f in fatias.items() if desde < c <= ate):
        return "parcial", "Em andamento"
    return "pendente", "Pendente"


def _texto(texto: str) -> str:
    """Escapa e mostra `trechos` em código, como no Markdown das specs."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escape(texto))


def _barra(pct: int, rotulo: str) -> str:
    return (
        f'<div class="barra" role="progressbar" aria-valuenow="{pct}" aria-valuemin="0" aria-valuemax="100" '
        f'aria-label="{escape(rotulo)}"><span style="width:{pct}%"></span></div>'
    )


def _lista(texto: str) -> str:
    itens = [i.strip() for i in texto.split("|") if i.strip()]
    return "".join(f"<li>{_texto(i)}</li>" for i in itens) or "<li>Nenhum</li>"


def _etapas(atual: int) -> str:
    passos = []
    for n, nome in enumerate(ETAPAS, start=1):
        estado = "feita" if n < atual else "atual" if n == atual else "futura"
        marca = "✓" if estado == "feita" else str(n)
        aria = ' aria-current="step"' if estado == "atual" else ""
        passos.append(f'<li class="{estado}"{aria}><span class="num">{marca}</span>{nome}</li>')
    return f'<ol class="etapas">{"".join(passos)}</ol>'


def _tarefas(fatia: Fatia) -> str:
    if not fatia.tarefas:
        return '<p class="mudo">Sem tarefas planejadas.</p>'
    linhas = []
    for t in fatia.tarefas:
        estado = "feita" if t.feita else "adiada" if t.adiada else "aberta"
        marca = {"feita": "✓", "adiada": "⏸", "aberta": "○"}[estado]
        etiqueta = ' <span class="chip adiada">adiada</span>' if t.adiada else ""
        linhas.append(
            f'<li class="{estado}"><span class="marca" aria-hidden="true">{marca}</span>'
            f"<b>{t.codigo}</b> {_texto(t.titulo)}{etiqueta}</li>"
        )
    return f'<ul class="tarefas">{"".join(linhas)}</ul>'


def gerar() -> str:
    fatias = _fatias()
    por_codigo = {f.codigo: f for f in fatias}
    andamento = _em_andamento()
    atual = por_codigo.get(andamento.get("Fatia", ""))
    etapa = int(andamento.get("Etapa", "1"))
    total = sum(len(f.tarefas) for f in fatias)
    feitas = sum(f.feitas for f in fatias)
    pct_geral = round(100 * feitas / total) if total else 0

    tarefa_atual = ""
    if atual:
        proxima = next((t for t in atual.tarefas if not t.feita and not t.adiada), None)
        if etapa == 3 and proxima:
            tarefa_atual = f"<p>Tarefa atual: <b>{proxima.codigo}</b> {escape(proxima.titulo)}</p>"

    gates = "".join(
        f'<li class="gate {estado}"><b>{g}</b> {escape(nome)} '
        f'<span class="chip {estado}">{rotulo}</span></li>'
        for (g, nome, ate), desde in zip(GATES, ["", "F00", "F03"], strict=True)
        for estado, rotulo in [_gate(por_codigo, desde, ate)]
    )

    linhas = []
    for f in fatias:
        destaque = " atual" if f is atual else ""
        etapa_f = etapa if f is atual else f.etapa()
        nome_etapa = "Concluída" if etapa_f == 6 else f"{etapa_f}/5 {ETAPAS[etapa_f - 1]}"
        status_css = "s" + str(STATUS_ORDEM.index(f.status)) if f.status in STATUS_ORDEM else "s0"
        contagem = f"{f.feitas}/{len(f.tarefas)} · {f.pct}%"
        linhas.append(f"""
      <details class="fatia{destaque}"{" open" if f is atual else ""}>
        <summary>
          <span class="cod">{f.codigo}</span>
          <span class="nome">{escape(f.nome)}<small>{escape(f.release)}</small></span>
          <span class="chip {status_css}">{escape(f.status)}</span>
          <span class="etapa">{nome_etapa}</span>
          <span class="prog">{_barra(f.pct, f"{f.codigo}: {f.pct}%")}<small>{contagem}</small></span>
        </summary>
        {_tarefas(f)}
      </details>""")

    branch, commit = _git("branch", "--show-current"), _git("rev-parse", "--short", "HEAD")
    gerado = datetime.now().strftime("%d/%m/%Y %H:%M")
    titulo_atual = f"{atual.codigo} – {escape(atual.nome)}" if atual else "Nenhuma"

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EAP do projeto</title>
<style>
:root {{
  --fundo:#f6f7f9; --cartao:#fff; --texto:#17202a; --mudo:#5b6673; --borda:#dfe3e8;
  --acento:#1f5fbf; --ok:#1d7a46; --ok-fundo:#e3f4ea; --aviso:#8a5a00; --aviso-fundo:#fdf1d8;
  --neutro-fundo:#eef1f4; --barra:#e4e8ed;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --fundo:#11151a; --cartao:#1a2028; --texto:#e6eaef; --mudo:#9aa5b1; --borda:#2c3540;
    --acento:#6ea3ff; --ok:#5fd08f; --ok-fundo:#183326; --aviso:#f0c062; --aviso-fundo:#3a2d12;
    --neutro-fundo:#242c36; --barra:#2a333d;
  }}
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--fundo); color:var(--texto);
  font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
main {{ max-width:1000px; margin:0 auto; padding:24px 16px 48px; }}
h1 {{ font-size:22px; margin:0; }} h2 {{ font-size:16px; margin:0 0 12px; }}
.meta {{ color:var(--mudo); font-size:13px; margin:4px 0 20px; }}
.grade {{ display:grid; gap:16px; grid-template-columns:2fr 1fr; margin-bottom:16px; }}
@media (max-width:720px) {{ .grade {{ grid-template-columns:1fr; }} }}
.cartao {{ background:var(--cartao); border:1px solid var(--borda); border-radius:10px; padding:16px; }}
.destaque {{ font-size:18px; font-weight:600; margin:0 0 12px; }}
.etapas {{ list-style:none; display:flex; gap:6px; padding:0; margin:0 0 12px; flex-wrap:wrap; }}
.etapas li {{ flex:1 1 90px; display:flex; align-items:center; gap:6px; padding:6px 8px; border-radius:8px;
  background:var(--neutro-fundo); color:var(--mudo); font-size:13px; }}
.etapas .num {{ display:inline-grid; place-items:center; width:20px; height:20px; border-radius:50%;
  border:1px solid currentColor; font-size:11px; flex:none; }}
.etapas .feita {{ background:var(--ok-fundo); color:var(--ok); }}
.etapas .atual {{ background:var(--acento); color:#fff; font-weight:600; }}
.colunas {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
@media (max-width:560px) {{ .colunas {{ grid-template-columns:1fr; }} }}
.colunas h3 {{ font-size:13px; color:var(--mudo); margin:8px 0 4px;
  text-transform:uppercase; letter-spacing:.04em; }}
.colunas ol, .colunas ul {{ margin:0; padding-left:20px; }}
.numero {{ font-size:34px; font-weight:700; line-height:1; }}
.barra {{ height:8px; background:var(--barra); border-radius:99px; overflow:hidden; }}
.barra span {{ display:block; height:100%; background:var(--acento); }}
.gates {{ list-style:none; padding:0; margin:12px 0 0; display:grid; gap:6px; font-size:13px; }}
.chip {{ display:inline-block; font-size:12px; padding:1px 8px; border-radius:99px;
  background:var(--neutro-fundo); color:var(--mudo); white-space:nowrap; }}
.chip.feito, .chip.s3, .chip.s4 {{ background:var(--ok-fundo); color:var(--ok); }}
.chip.parcial, .chip.s1, .chip.s2, .chip.adiada {{ background:var(--aviso-fundo); color:var(--aviso); }}
.fatia {{ background:var(--cartao); border:1px solid var(--borda); border-radius:10px; margin-bottom:8px; }}
.fatia.atual {{ border-color:var(--acento); box-shadow:0 0 0 1px var(--acento); }}
summary {{ display:grid; grid-template-columns:44px 1fr auto 130px 150px; gap:10px; align-items:center;
  padding:10px 14px; cursor:pointer; list-style:none; }}
summary::-webkit-details-marker {{ display:none; }}
summary small {{ display:block; color:var(--mudo); font-size:12px; }}
@media (max-width:720px) {{
  summary {{ grid-template-columns:44px 1fr auto; }} .etapa, .prog {{ grid-column:2 / -1; }}
}}
.cod {{ font-weight:700; color:var(--acento); }} .etapa {{ font-size:13px; color:var(--mudo); }}
.tarefas {{ list-style:none; margin:0; padding:4px 14px 14px 68px; display:grid; gap:4px; font-size:14px; }}
@media (max-width:720px) {{ .tarefas {{ padding-left:14px; }} }}
.tarefas .marca {{ display:inline-block; width:18px; }}
.tarefas .feita {{ color:var(--mudo); }} .tarefas .feita .marca {{ color:var(--ok); }}
.mudo {{ color:var(--mudo); padding:0 14px 14px 68px; margin:0; }}
</style>
</head>
<body>
<main>
  <h1>EAP · Sistema de Gestão PDCA e SDCA</h1>
  <p class="meta">Gerada em {gerado} · branch <code>{escape(branch)}</code> @ <code>{escape(commit)}</code>
    · fonte: <code>specs/README.md</code> e <code>specs/Fxx-*/tasks.md</code></p>

  <div class="grade">
    <section class="cartao" aria-labelledby="t-andamento">
      <h2 id="t-andamento">Fatia em andamento</h2>
      <p class="destaque">{titulo_atual}</p>
      {_etapas(etapa)}
      {tarefa_atual}
      <div class="colunas">
        <div><h3>Próximos passos</h3><ol>{_lista(andamento.get("Próximos passos", ""))}</ol></div>
        <div><h3>Bloqueios e decisões</h3><ul>{_lista(andamento.get("Bloqueios", ""))}</ul></div>
      </div>
    </section>
    <section class="cartao" aria-labelledby="t-geral">
      <h2 id="t-geral">Progresso geral</h2>
      <p class="numero">{pct_geral}%</p>
      <p class="meta" style="margin:4px 0 8px">{feitas} de {total} tarefas planejadas</p>
      {_barra(pct_geral, f"Progresso geral: {pct_geral}%")}
      <ul class="gates">{gates}</ul>
    </section>
  </div>

  <section aria-labelledby="t-fatias">
    <h2 id="t-fatias">Fatias (clique para ver as tarefas)</h2>
    {"".join(linhas)}
  </section>
</main>
</body>
</html>
"""


if __name__ == "__main__":
    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text(gerar(), "utf-8")
    print(f"EAP gerada: {SAIDA}")

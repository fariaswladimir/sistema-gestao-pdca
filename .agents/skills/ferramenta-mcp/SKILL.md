---
name: ferramenta-mcp
description: Use ao criar ou alterar ferramentas, recursos ou prompts do servidor MCP do sistema.
---

# Ferramenta MCP

Arquivos: `backend/app/mcp/servidor.py` (registro), `backend/app/mcp/ferramentas/<nome>.py`.

Modelo:
```python
from app.mcp.base import ferramenta, ContextoMCP
from app.servicos.indicadores import ServicoIndicadores
from pydantic import BaseModel, Field

class Entrada(BaseModel):
    indicador_id: str = Field(description="ID do indicador")
    meses: int = Field(12, ge=1, le=36, description="Quantidade de meses da série")

@ferramenta(nome="consultar_indicador", acao="indicador:ler", escrita=False)
async def consultar_indicador(entrada: Entrada, ctx: ContextoMCP) -> dict:
    dados = await ServicoIndicadores(ctx.sessao, ctx.usuario).detalhar(entrada.indicador_id, entrada.meses)
    return ctx.resposta(texto=f"{dados.nome}: farol {dados.farol_atual}", dados=dados.model_dump())
```

Checklist:
1. O decorator aplica permissão (`acao`) com o usuário do token; não reimplemente.
2. Use o mesmo serviço da API. Nunca SQL direto na ferramenta.
3. `escrita=True` obriga o serviço a criar rascunho/pendente e registra auditoria com `ator_tipo='ia'`.
4. Descrição da ferramenta curta, dizendo quando usar e o que devolve.
5. Atualize `specs/Fxx-*/contracts/mcp-tools.json` e o teste de contrato.
6. Teste: sucesso, entrada inválida, usuário sem permissão, usuário de outro setor.

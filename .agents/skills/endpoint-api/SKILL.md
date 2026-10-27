---
name: endpoint-api
description: Use ao criar ou alterar rotas REST do backend FastAPI.
---

# Endpoint de API

```python
@router.post("/anomalias/{anomalia_id}/causas", response_model=CausaSaida, status_code=201)
async def registrar_causa(
    anomalia_id: UUID,
    entrada: CausaEntrada,
    usuario: Usuario = Depends(exigir_permissao("anomalia:editar")),
    sessao: AsyncSession = Depends(sessao_db),
):
    return await ServicoAnomalias(sessao, usuario).registrar_causa(anomalia_id, entrada)
```

Checklist:
1. Rota fina: valida, autoriza, delega ao serviço.
2. Serviço aplica `escopo_setores` e audita escritas.
3. Erros de domínio viram 404 (fora do escopo também é 404, para não vazar existência), 409 ou 422.
4. Adicione a ação na matriz `tests/permissions/matriz.yaml` para todos os perfis.
5. Regere o cliente do frontend (`make api-client`).

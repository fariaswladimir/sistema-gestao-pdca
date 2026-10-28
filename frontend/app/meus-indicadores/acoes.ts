"use server";

import { revalidatePath } from "next/cache";

import { clienteApi, type Farol } from "@/lib/api/cliente";

export type ResultadoLancamento =
  | { ok: true; periodo: string; valor: number; farol: Farol }
  | { ok: false; codigo: string; detalhe: string };

export async function lancarMedicao(
  indicadorId: string,
  periodo: string,
  valor: number,
  justificativa: string | null,
): Promise<ResultadoLancamento> {
  const api = await clienteApi();
  if (!api) return { ok: false, codigo: "nao_autenticado", detalhe: "Sua sessão expirou. Entre novamente." };

  const { data, error } = await api.PUT("/indicadores/{indicador_id}/medicoes/{periodo}", {
    params: { path: { indicador_id: indicadorId, periodo } },
    body: { valor, justificativa },
  });
  if (error) return { ok: false, codigo: error.codigo, detalhe: error.detalhe };

  revalidatePath("/meus-indicadores");
  return { ok: true, periodo: data.periodo, valor: data.valor, farol: data.farol };
}

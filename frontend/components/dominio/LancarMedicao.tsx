"use client";

import { useId, useState, useTransition } from "react";

import { lancarMedicao } from "@/app/meus-indicadores/acoes";
import { lerNumero, numero, periodo as formatarPeriodo } from "@/lib/formato";

import { textoFarol } from "./Farol";

type Props = {
  indicadorId: string;
  periodoAtual: string;
  valorAtual: number | null;
};

export function LancarMedicao({ indicadorId, periodoAtual, valorAtual }: Props) {
  const id = useId();
  const [periodo, setPeriodo] = useState(periodoAtual);
  const [valor, setValor] = useState("");
  const [justificativa, setJustificativa] = useState("");
  const [exigidaPelaApi, setExigidaPelaApi] = useState(false);
  const [erro, setErro] = useState<string | null>(null);
  const [aviso, setAviso] = useState<string | null>(null);
  const [enviando, iniciar] = useTransition();

  // RN3: período que já tem valor exige justificativa. Para o período atual já sabemos;
  // para outros, a API avisa (código justificativa_obrigatoria) e o campo aparece.
  const pedeJustificativa = exigidaPelaApi || (periodo === periodoAtual && valorAtual !== null);

  function enviar(evento: React.FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setErro(null);
    setAviso(null);
    const numeroLido = lerNumero(valor);
    if (numeroLido === null) {
      setErro("Informe um número.");
      return;
    }
    iniciar(async () => {
      const resultado = await lancarMedicao(
        indicadorId,
        periodo,
        numeroLido,
        pedeJustificativa ? justificativa : null,
      );
      if (!resultado.ok) {
        if (resultado.codigo === "justificativa_obrigatoria") setExigidaPelaApi(true);
        setErro(resultado.detalhe);
        return;
      }
      setAviso(
        `Lançado ${numero(resultado.valor)} em ${formatarPeriodo(resultado.periodo)}: ${textoFarol(resultado.farol)}.`,
      );
      setValor("");
      setJustificativa("");
      setExigidaPelaApi(false);
    });
  }

  return (
    <form onSubmit={enviar} className="mt-4 grid gap-3 sm:grid-cols-[auto_auto_1fr_auto] sm:items-end">
      <label className="grid gap-1 text-sm" htmlFor={`${id}-periodo`}>
        Período
        <input
          id={`${id}-periodo`}
          type="month"
          required
          value={periodo}
          onChange={(e) => {
            setPeriodo(e.target.value);
            setExigidaPelaApi(false);
          }}
          className="rounded border border-slate-300 px-2 py-1"
        />
      </label>
      <label className="grid gap-1 text-sm" htmlFor={`${id}-valor`}>
        Valor
        <input
          id={`${id}-valor`}
          inputMode="decimal"
          required
          value={valor}
          onChange={(e) => setValor(e.target.value)}
          className="w-32 rounded border border-slate-300 px-2 py-1"
        />
      </label>
      {pedeJustificativa ? (
        <label className="grid gap-1 text-sm" htmlFor={`${id}-justificativa`}>
          Justificativa da correção
          <input
            id={`${id}-justificativa`}
            value={justificativa}
            onChange={(e) => setJustificativa(e.target.value)}
            maxLength={1000}
            className="rounded border border-slate-300 px-2 py-1"
          />
        </label>
      ) : (
        <span />
      )}
      <button
        type="submit"
        disabled={enviando}
        className="rounded bg-slate-900 px-4 py-1.5 text-sm font-medium text-white disabled:opacity-50"
      >
        {enviando ? "Lançando…" : "Lançar"}
      </button>
      <p aria-live="polite" className="text-sm sm:col-span-4">
        {erro && (
          <span role="alert" className="text-red-700">
            {erro}
          </span>
        )}
        {aviso && <span className="text-green-800">{aviso}</span>}
      </p>
    </form>
  );
}

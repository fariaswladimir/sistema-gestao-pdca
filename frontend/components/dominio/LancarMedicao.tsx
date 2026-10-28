"use client";

import { useId, useState, useTransition } from "react";

import { lancarMedicao } from "@/app/meus-indicadores/acoes";
import { Botao } from "@/components/ui/Botao";
import { Campo } from "@/components/ui/Campo";
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
    <form
      onSubmit={enviar}
      className="mt-4 grid gap-3 border-t border-borda pt-4 sm:grid-cols-[auto_auto_1fr_auto] sm:items-end"
    >
      <Campo
        id={`${id}-periodo`}
        rotulo="Período"
        type="month"
        required
        value={periodo}
        onChange={(e) => {
          setPeriodo(e.target.value);
          setExigidaPelaApi(false);
        }}
      />
      <Campo
        id={`${id}-valor`}
        rotulo="Valor"
        inputMode="decimal"
        required
        value={valor}
        onChange={(e) => setValor(e.target.value)}
        className="w-32"
      />
      {pedeJustificativa ? (
        <Campo
          id={`${id}-justificativa`}
          rotulo="Justificativa da correção"
          value={justificativa}
          onChange={(e) => setJustificativa(e.target.value)}
          maxLength={1000}
        />
      ) : (
        <span />
      )}
      <Botao type="submit" aparencia="primaria" disabled={enviando}>
        {enviando ? "Lançando…" : "Lançar"}
      </Botao>
      <p aria-live="polite" className="sm:col-span-4">
        {erro && (
          <span role="alert" className="text-perigo-texto">
            {erro}
          </span>
        )}
        {aviso && <span className="text-sucesso-texto">{aviso}</span>}
      </p>
    </form>
  );
}

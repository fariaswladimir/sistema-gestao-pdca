import { redirect } from "next/navigation";

import { clienteApi } from "@/lib/api/cliente";

const ENTRAR = "/entrar?volta=/meus-indicadores";

export default async function MeusIndicadores() {
  const api = await clienteApi();
  if (!api) redirect(ENTRAR);

  const eu = await api.GET("/eu");
  if (eu.response.status === 401) redirect(ENTRAR);
  if (!eu.data) {
    return (
      <p role="alert" className="rounded border border-amber-300 bg-amber-50 p-4">
        Seu usuário não tem cadastro ativo no sistema. Procure o escritório de gestão.
      </p>
    );
  }

  return (
    <section>
      <h1 className="text-2xl font-semibold">Meus indicadores</h1>
      <p className="mt-1 text-slate-600">Olá, {eu.data.nome}.</p>
      {/* T14: cartões com farol e lançamento */}
    </section>
  );
}

import { redirect } from "next/navigation";

import { CartaoIndicador } from "@/components/dominio/CartaoIndicador";
import { clienteApi } from "@/lib/api/cliente";

const ENTRAR = "/entrar?volta=/meus-indicadores";

export default async function MeusIndicadores() {
  const api = await clienteApi();
  if (!api) redirect(ENTRAR);

  const [eu, meus] = await Promise.all([api.GET("/eu"), api.GET("/indicadores/meus")]);
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
      {meus.data && meus.data.length > 0 ? (
        <div className="mt-6 grid gap-4">
          {meus.data.map((indicador) => (
            <CartaoIndicador key={indicador.id} indicador={indicador} />
          ))}
        </div>
      ) : (
        <p className="mt-6 text-slate-600">Você ainda não é responsável por nenhum indicador.</p>
      )}
    </section>
  );
}

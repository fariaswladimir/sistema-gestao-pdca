import { redirect } from "next/navigation";

import { destinoSeguro, modoLocal } from "@/lib/sessao";

import { escolherUsuario } from "./acoes";

type UsuarioLocal = { id: string; nome: string; setor: string };

async function usuarios(): Promise<UsuarioLocal[]> {
  const resposta = await fetch(`${process.env.API_URL}/sessao-local/usuarios`, { cache: "no-store" });
  return resposta.ok ? resposta.json() : [];
}

export default async function EscolherUsuario({
  searchParams,
}: {
  searchParams: Promise<{ volta?: string }>;
}) {
  if (!modoLocal()) redirect("/entrar");
  const volta = destinoSeguro((await searchParams).volta);
  const lista = await usuarios();

  return (
    <section>
      <h1 className="text-2xl font-semibold">Entrar</h1>
      <p className="mt-1 text-slate-600">
        Versão local, sem senha: escolha com qual colaborador quer usar o sistema.
      </p>
      {lista.length > 0 ? (
        <ul className="mt-6 grid gap-2 sm:grid-cols-2">
          {lista.map((usuario) => (
            <li key={usuario.id}>
              <form action={escolherUsuario}>
                <input type="hidden" name="id" value={usuario.id} />
                <input type="hidden" name="volta" value={volta} />
                <button
                  type="submit"
                  className="w-full rounded-lg border border-slate-200 bg-white px-4 py-3 text-left shadow-sm hover:border-slate-400 focus:outline-none focus-visible:ring-2 focus-visible:ring-slate-900"
                >
                  <span className="block font-medium">{usuario.nome}</span>
                  <span className="block text-sm text-slate-600">{usuario.setor}</span>
                </button>
              </form>
            </li>
          ))}
        </ul>
      ) : (
        <p role="alert" className="mt-6 rounded border border-amber-300 bg-amber-50 p-4">
          Nenhum colaborador cadastrado. Rode <code>make seed</code> para carregar os dados de exemplo.
        </p>
      )}
    </section>
  );
}

import { redirect } from "next/navigation";

import { CLASSE_FOCO } from "@/components/ui/Botao";
import { MensagemSecao } from "@/components/ui/MensagemSecao";
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
      <h1 className="text-titulo-grande font-semibold">Entrar</h1>
      <p className="mt-1 text-texto-sutil">
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
                  className={`w-full rounded-lg bg-superficie-elevada px-4 py-3 text-left shadow-elevada hover:bg-fundo-selecionado ${CLASSE_FOCO}`}
                >
                  <span className="block font-semibold">{usuario.nome}</span>
                  <span className="block text-texto-sutil">{usuario.setor}</span>
                </button>
              </form>
            </li>
          ))}
        </ul>
      ) : (
        <div className="mt-6">
          <MensagemSecao papel="alerta" titulo="Nenhum colaborador cadastrado">
            Rode <code>make seed</code> para carregar os dados de exemplo.
          </MensagemSecao>
        </div>
      )}
    </section>
  );
}

import type { Metadata } from "next";

import { cabecalhosDaSessao } from "@/lib/sessao";

import { sair } from "./acoes-sessao";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sistema de Gestão PDCA",
  description: "Metas, indicadores e farol do mês",
};

export default async function Layout({ children }: { children: React.ReactNode }) {
  const logado = (await cabecalhosDaSessao()) !== null;
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-slate-50 text-slate-900">
        <header className="border-b border-slate-200 bg-white">
          <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
            <span className="font-semibold">Sistema de Gestão PDCA</span>
            {logado && (
              <form action={sair}>
                <button type="submit" className="text-sm text-slate-600 underline hover:text-slate-900">
                  Sair
                </button>
              </form>
            )}
          </div>
        </header>
        <main className="mx-auto max-w-4xl px-4 py-6">{children}</main>
      </body>
    </html>
  );
}

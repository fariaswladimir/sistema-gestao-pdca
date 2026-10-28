import type { Metadata } from "next";

import { Botao } from "@/components/ui/Botao";
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
      <body className="min-h-screen">
        <header className="border-b border-borda bg-superficie">
          <div className="mx-auto flex h-14 max-w-4xl items-center justify-between px-4">
            <span className="text-titulo-pequeno font-semibold">Sistema de Gestão PDCA</span>
            {logado && (
              <form action={sair}>
                <Botao type="submit" aparencia="sutil">
                  Sair
                </Botao>
              </form>
            )}
          </div>
        </header>
        <main className="mx-auto max-w-4xl px-4 py-6">{children}</main>
      </body>
    </html>
  );
}

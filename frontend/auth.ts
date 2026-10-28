import NextAuth from "next-auth";
import type { JWT } from "next-auth/jwt";
import Keycloak from "next-auth/providers/keycloak";

declare module "next-auth" {
  interface Session {
    accessToken?: string;
    erro?: "RenovacaoFalhou";
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    accessToken?: string;
    refreshToken?: string;
    idToken?: string; // só no servidor: id_token_hint do logout no Keycloak
    expiraEm?: number;
    erro?: "RenovacaoFalhou";
  }
}

const MARGEM_S = 30;

/** O access token do Keycloak dura 5 min; renova com o refresh token antes de vencer. */
async function renovar(token: JWT): Promise<JWT> {
  try {
    const resposta = await fetch(`${process.env.AUTH_KEYCLOAK_ISSUER}/protocol/openid-connect/token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "refresh_token",
        refresh_token: token.refreshToken ?? "",
        client_id: process.env.AUTH_KEYCLOAK_ID ?? "",
        client_secret: process.env.AUTH_KEYCLOAK_SECRET ?? "",
      }),
    });
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.error ?? "falha ao renovar");
    return {
      ...token,
      accessToken: dados.access_token,
      refreshToken: dados.refresh_token ?? token.refreshToken,
      idToken: dados.id_token ?? token.idToken,
      expiraEm: Math.floor(Date.now() / 1000) + dados.expires_in,
      erro: undefined,
    };
  } catch {
    return { ...token, erro: "RenovacaoFalhou" };
  }
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [Keycloak],
  session: { strategy: "jwt" },
  callbacks: {
    async jwt({ token, account }) {
      if (account) {
        return {
          ...token,
          accessToken: account.access_token,
          refreshToken: account.refresh_token,
          idToken: account.id_token,
          expiraEm: account.expires_at,
        };
      }
      if (token.expiraEm && Date.now() / 1000 < token.expiraEm - MARGEM_S) return token;
      return renovar(token);
    },
    session({ session, token }) {
      session.accessToken = token.accessToken;
      session.erro = token.erro;
      return session;
    },
  },
});

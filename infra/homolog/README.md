# Homologação

Um servidor interno com Docker roda `docker-compose.homolog.yml`. Cada merge na `main` passa pelo CI,
publica as imagens no GHCR e o job `deploy-homologacao`, que roda num runner do GitHub Actions instalado
no próprio servidor, atualiza o ambiente. O runner só faz conexões de saída para o GitHub, sem nenhuma porta aberta.

| Endereço | O quê |
| --- | --- |
| `https://HOMOLOG_HOST/` | Aplicação |
| `https://HOMOLOG_HOST/auth/admin/` | Console do Keycloak (cadastro de usuários) |
| `https://HOMOLOG_HOST:3443/` | Uptime Kuma (monitoramento) |

O banco, a API e o Keycloak não ficam expostos: só o Caddy publica as portas 80, 443 e 3443.

## 1. Preparar o servidor (uma vez)
Requisitos: Linux com Docker Engine e o plugin Compose v2, 2 vCPU, 4 GB de RAM e 20 GB de disco.
O servidor precisa de saída HTTPS para `github.com` e `ghcr.io`, e de um nome no DNS interno (`HOMOLOG_HOST`).

```sh
sudo mkdir -p /opt/gestao-pdca/certs
sudo cp infra/homolog/homolog.env.example /opt/gestao-pdca/homolog.env
sudo chmod 600 /opt/gestao-pdca/homolog.env   # dono: o usuário do runner
# preencha HOMOLOG_HOST e cada segredo com: openssl rand -hex 32
```

### Certificado HTTPS
- **CA interna do Caddy** (`CADDY_TLS=internal`, padrão): funciona sem nada pedido à TI. Os navegadores alertam
  até que a raiz seja instalada nas máquinas de quem vai usar. Para obter a raiz:
  `docker compose -f docker-compose.homolog.yml --env-file /opt/gestao-pdca/homolog.env exec caddy cat /ca/root.crt`.
- **Certificado da organização**: coloque `cert.pem` (com a cadeia), `chave.pem` e `ca-organizacao.pem` em
  `/opt/gestao-pdca/certs` e defina `CADDY_TLS=/certs/cert.pem /certs/chave.pem` e
  `NODE_EXTRA_CA_CERTS=/certs/ca-organizacao.pem`.

## 2. Instalar o runner (uma vez)
1. No GitHub, em *Settings → Actions → Runners → New self-hosted runner*, escolha Linux e siga os comandos
   num usuário próprio (por exemplo, `gh-runner`) que esteja no grupo `docker`.
2. Em `./config.sh`, informe o rótulo extra **`homologacao`**. Depois rode `sudo ./svc.sh install && sudo ./svc.sh start`.
3. Em *Settings → Environments*, crie `homologacao`. Opcional: exija aprovação antes de cada deploy.
4. Em *Settings → Secrets and variables → Actions → Variables*, crie `HOMOLOG_HOST` (o nome) e
   **`HOMOLOG_ATIVA=true`**. Sem essa variável o job não roda, e o CI não fica esperando um runner inexistente.

## 3. Primeira subida
Rode no servidor, a partir de um clone do repositório (o runner usa o mesmo script):
```sh
echo <PAT com read:packages> | docker login ghcr.io -u <usuário> --password-stdin
SEMEAR=1 infra/homolog/implantar.sh
```
O script baixa as imagens, sobe tudo e espera os healthchecks. Depois aplica as migrações,
carrega os dados de exemplo (com `SEMEAR=1`), confere a versão em `/saude` e testa a web pelo HTTPS.

Os usuários de demonstração (ana, bruno, carlos, duda, eva e root) entram com `KC_SENHA_INICIAL` e precisam
trocar a senha no primeiro acesso. O realm só é importado na primeira subida. Depois disso, usuários e
configurações se gerenciam no console do Keycloak, e mudar `realm-gestao.json` não tem efeito.

## 4. Monitoramento (uma vez, no Uptime Kuma)
Abra `https://HOMOLOG_HOST:3443`, crie a conta de administrador e então:
1. Em *Configurações → Notificações*, crie uma notificação SMTP com o servidor de e-mail da organização
   e marque "aplicar a todos os monitores".
2. Crie o monitor **API** do tipo HTTP(s) – Palavra-chave, URL `http://api:8000/saude`, palavra-chave `"banco":"ok"`
   e intervalo de 60 s. Ele alerta quando a API cai ou perde o banco.
3. Crie o monitor **Web** do tipo HTTP(s), URL `http://web:3000/`, intervalo de 60 s, com 300–399 nos códigos aceitos.
4. Crie o monitor **Login** do tipo HTTP(s), URL `http://keycloak:8080/auth/realms/gestao`, intervalo de 60 s.
5. Teste o alerta: `docker compose ... stop api`. O e-mail deve chegar em até 2 minutos. Depois rode `start api`.

## Operação
Antes de cada comando, defina:
`dc() { docker compose -f docker-compose.homolog.yml --env-file /opt/gestao-pdca/homolog.env "$@"; }`

- **Erros da aplicação:** os logs saem em JSON, com rotação de 5 arquivos de 10 MB por serviço.
  Para ver só os erros: `dc logs --since 24h api worker | grep '"level": "error"'`.
- **Estado dos serviços:** `dc ps`. Um worker travado aparece como `unhealthy`.
- **Voltar para uma versão anterior:** `VERSAO=<sha anterior> infra/homolog/implantar.sh`. As migrações só
  avançam, então volte apenas para uma versão com o mesmo esquema de banco.
- **Backup do banco:** fora do escopo da F00. Para um backup manual:
  `dc exec -T db pg_dumpall -U gestao > backup.sql`.

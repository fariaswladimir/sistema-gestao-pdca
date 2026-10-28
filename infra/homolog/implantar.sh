#!/usr/bin/env bash
# Implanta ou atualiza a homologação e confere que a versão pedida está no ar.
# Uso (na raiz do repositório, no servidor): VERSAO=<sha do commit> infra/homolog/implantar.sh
#   HOMOLOG_ENV  arquivo de ambiente (padrão /opt/gestao-pdca/homolog.env)
#   SEM_PULL=1   usa imagens já presentes (teste local)
#   SEMEAR=1     carrega os dados de exemplo (idempotente)
set -euo pipefail
cd "$(dirname "$0")/../.."

HOMOLOG_ENV="${HOMOLOG_ENV:-/opt/gestao-pdca/homolog.env}"
export VERSAO="${VERSAO:-main}"
HOMOLOG_HOST=$(sed -n 's/^HOMOLOG_HOST=//p' "$HOMOLOG_ENV")

dc() { docker compose -f docker-compose.homolog.yml --env-file "$HOMOLOG_ENV" "$@"; }

[ -n "${SEM_PULL:-}" ] || dc pull --quiet
dc up -d --wait --wait-timeout 600 --remove-orphans
dc exec -T api alembic upgrade head
[ -z "${SEMEAR:-}" ] || dc exec -T api python -m app.seed

versao=$(dc exec -T api python -c \
  "import json,urllib.request; print(json.load(urllib.request.urlopen('http://localhost:8000/saude'))['versao'])")
if [ "$VERSAO" != main ] && [ "$versao" != "$VERSAO" ]; then
  echo "::error::/saude responde versão $versao, esperada $VERSAO" >&2
  exit 1
fi

# a web responde pelo Caddy (HTTPS); -k porque o servidor pode não confiar na CA interna
curl -fsSk -o /dev/null --resolve "$HOMOLOG_HOST:443:127.0.0.1" "https://$HOMOLOG_HOST/"
echo "homologação no ar: https://$HOMOLOG_HOST (versão $versao)"

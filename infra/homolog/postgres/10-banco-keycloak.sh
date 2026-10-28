#!/bin/sh
# Roda só na criação do volume: banco e usuário próprios do Keycloak no mesmo Postgres.
set -e
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<SQL
CREATE ROLE keycloak LOGIN PASSWORD '$KC_DB_PASSWORD';
CREATE DATABASE keycloak OWNER keycloak;
SQL

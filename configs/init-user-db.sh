#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    create user "$CTFORCES_DB_USER" with password '$CTFORCES_DB_PASSWORD';
    alter role "$CTFORCES_DB_USER" set client_encoding to 'utf8';
    create database "$CTFORCES_DB_NAME" owner "$CTFORCES_DB_USER";
EOSQL
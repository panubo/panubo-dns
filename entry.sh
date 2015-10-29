#!/usr/bin/env bash

set -ex

function genpasswd() {
    export LC_CTYPE=C  # Quiet tr warnings
    local l=$1
    [ "$l" == "" ] && l=16
    cat /dev/urandom | tr -dc A-Za-z0-9_ | head -c ${l}
}

# Set Secret Key if Debug enabled
if [ "$DEBUG" == "true" ]; then
    export SECRET_KEY=${SECRET_KEY:-$(genpasswd 32)}
fi

# App Defaults
export WORKERS=${WORKERS-4}
export LOGFILE=${LOGFILE-/srv/log/web.log}
export PORT=${PORT-8000}

# alias docker links variables

# COUCHDB SERVICE
export COUCHDB_DNS_NAME="${COUCHDB_ENV_COUCHDB_DATABASE}"
export COUCHDB_DNS_USER="${COUCHDB_ENV_COUCHDB_USER}"
export COUCHDB_DNS_PASS="${COUCHDB_ENV_COUCHDB_PASS}"
export COUCHDB_DNS_HOST="http://${COUCHDB_PORT_5984_TCP_ADDR}:${COUCHDB_PORT_5984_TCP_PORT}"

# SMTP SERVICE
export EMAIL_HOST="${EMAIL_HOST-${SMTP_PORT_25_TCP_ADDR-localhost}}"
export EMAIL_PORT="${EMAIL_PORT-${SMTP_PORT_25_TCP_PORT-25}}"

# MYSQL SERVICE
if [ -z "$DATABASE_URL" ]; then
    export DATABASE_URL="mysql://${DB_USER}:${DB_PASS}@${DB_HOST-$MARIADB_PORT_3306_TCP_ADDR}:${DB_PORT-$MARIADB_PORT_3306_TCP_PORT}/${DB_NAME}"
fi

echo "Exec'ing $@"
exec "$@"

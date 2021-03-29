#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


wait_for_postgres() {
    local timeout="${1:-60s}"
    local retry_interval="${2:-1s}"

    dockerize \
        -wait "tcp://${POSTGRES_HOST}:${POSTGRES_PORT}" \
        -wait-retry-interval "${retry_interval}" \
        -timeout "${timeout}"
}


# Ensure postgresql is started and ready to accept connections within 60s
>&2 echo 'Waiting for PostgreSQL..'
wait_for_postgres "60s"
>&2 echo 'PostgreSQL is available'

exec "$@"
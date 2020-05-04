#!/bin/bash

set -e

cd /app

case ${CELERY_CONTAINER_TYPE} in
"worker")
    echo "[*] Starting celery worker"
    celery worker -A ctforces_backend \
        -E -l info \
        --concurrency=20
    ;;
"flower")
    echo "[*] Starting celery flower"
    celery flower -A ctforces_backend \
        --basic_auth="$FLOWER_BASIC_AUTH" \
        --url-prefix=flower \
        --host=0.0.0.0 \
        --port=5555
    ;;
esac

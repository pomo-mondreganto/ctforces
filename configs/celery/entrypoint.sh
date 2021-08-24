#!/bin/bash -e

cd /app

case ${CELERY_CONTAINER_TYPE} in
"worker")
    echo "[*] Starting celery worker"
    celery -A ctforces \
        worker \
        -E -l info \
        --concurrency=20
    ;;
"flower")
    echo "[*] Starting celery flower"
    celery -A ctforces \
        flower \
        --basic_auth="$FLOWER_BASIC_AUTH" \
        --url-prefix=flower \
        --host=0.0.0.0 \
        --port=5555
    ;;
esac

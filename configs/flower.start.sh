#!/bin/sh


echo "[+] Starting Flower"
cd /app
celery -A ctforces_backend flower --basic_auth="$FLOWER_BASIC_AUTH" --url-prefix=flower --unix_socket=/socks/flower.sock

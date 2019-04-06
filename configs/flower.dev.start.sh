#!/bin/sh

echo "[+] Waiting 10 secs for celery to start"
sleep 10

echo "[+] Starting Flower"
cd /app
celery -A ctforces_backend flower --url-prefix=flower --unix_socket=/socks/flower.sock
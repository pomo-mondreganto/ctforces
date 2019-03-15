#!/bin/sh

#####
# Postgres: wait until container is created
#####

set +e
echo "[+] Checking is postgres container started"
python3 /db.check.py
while [[ $? != 0 ]] ; do
    sleep 3; echo "[*] Waiting for postgres container..."
    python3 /db.check.py
done
set -e

#####
# Django setup
#####

# Django: migrate
#
# Django will see that the tables for the initial migrations already exist
# and mark them as applied without running them. (Django won’t check that the
# table schema match your models, just that the right table names exist).
echo "[+] Django setup, executing: migrate"
python3 /app/manage.py migrate

echo "[+] Django setup, executing: collectstatic"
python3 /app/manage.py collectstatic --noinput -v 3

#####
# Start uWSGI
#####
echo "[+] Starting server..."
cd /app
gunicorn --access-logfile /logs/access.log \
 --error-logfile /logs/error.log \
  --worker-class gevent --worker-connections 768 --timeout 120 \
  --bind unix:/socks/ctforces.sock \
  ctforces_backend.wsgi:application

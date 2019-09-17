"""
db.check.py
This script will check whether the postgres container is up and running. It'll
connect to the database with the credentials provided in the environment
variables.
"""

import os
import sys

import psycopg2


def database_check():
    dbname = os.environ.get('CTFORCES_DB_NAME')
    user = os.environ.get('CTFORCES_DB_USER')
    password = os.environ.get('CTFORCES_DB_PASSWORD')
    host = os.environ.get('POSTGRES_HOST', 'ctforces-postgres')
    port = os.environ.get('POSTGRES_PORT', 5432)

    print("HOST: {host}:{port}, DB: {dbname}, USER: {user}".format(
        dbname=dbname,
        user=user,
        host=host,
        port=port))

    try:
        psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port)
    except:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    database_check()

#!/usr/bin/env python3

import argparse
import os
import secrets
import subprocess
import traceback

import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.yml')

DOCKER_COMPOSE_FILES = [os.path.join(BASE_DIR, 'docker-compose.yml')]


def run_command(command, cwd=None, env=None):
    p = subprocess.Popen(command, cwd=cwd, env=env)
    rc = p.wait()
    if rc != 0:
        print('[-] Failed!')
        exit(1)


def get_compose_files():
    return sum((['-f', f] for f in DOCKER_COMPOSE_FILES), [])


def setup_db(config):
    postgres_env_path = os.path.join(
        BASE_DIR,
        'configs',
        'postgres',
        'environment.env',
    )

    db_config = config['db']
    host = db_config['host']
    port = db_config['port']
    user = db_config['user']
    password = db_config['password']
    db = db_config['dbname']

    postgres_config = [
        "# THIS FILE IS MANAGED BY 'control.py'",
        f'POSTGRES_HOST={host}',
        f'POSTGRES_PORT={port}',
        f'POSTGRES_USER={user}',
        f'POSTGRES_PASSWORD={password}',
        f'POSTGRES_DB={db}',
    ]

    with open(postgres_env_path, 'w') as f:
        f.write('\n'.join(postgres_config))


def setup_flower(config):
    flower_env_path = os.path.join(
        BASE_DIR,
        'configs',
        'celery',
        'flower.env',
    )

    admin_config = config['flower']
    flower_username = admin_config['username']
    flower_password = admin_config['password']
    flower_config = [
        "# THIS FILE IS MANAGED BY 'control.py'",
        f'FLOWER_BASIC_AUTH={flower_username}:{flower_password}',
    ]

    with open(flower_env_path, 'w') as f:
        f.write('\n'.join(flower_config))


def setup_rabbitmq(config):
    rabbitmq_env_path = os.path.join(
        BASE_DIR,
        'configs',
        'rabbitmq',
        'environment.env',
    )

    rabbitmq_config = config['rabbitmq']
    host = rabbitmq_config['host']
    port = rabbitmq_config['port']
    user = rabbitmq_config['user']
    password = rabbitmq_config['password']
    vhost = rabbitmq_config['vhost']

    rabbitmq_config = [
        "# THIS FILE IS MANAGED BY 'control.py'",
        f'RABBITMQ_HOST={host}',
        f'RABBITMQ_PORT={port}',
        f'RABBITMQ_DEFAULT_USER={user}',
        f'RABBITMQ_DEFAULT_PASS={password}',
        f'RABBITMQ_DEFAULT_VHOST={vhost}',
    ]

    with open(rabbitmq_env_path, 'w') as f:
        f.write('\n'.join(rabbitmq_config))


def setup_django(config):
    django_env_path = os.path.join(
        BASE_DIR,
        'configs',
        'django',
        'environment.env',
    )

    django_config = config['django']
    debug = '1' if django_config['debug'] else '0'
    secret_key = django_config.get('secret_key') or secrets.token_hex(32)

    email_config = django_config['email']
    url = email_config['url']
    host = email_config['host']
    user = email_config['user']
    port = email_config['port']

    django_config = [
        "# THIS FILE IS MANAGED BY 'control.py'",
        f'DJANGO_DEBUG={debug}',
        f'DJANGO_SECRET_KEY={secret_key}',
        f'DJANGO_EMAIL_URL={url}',
        f'DJANGO_EMAIL_HOST={host}',
        f'DJANGO_EMAIL_USER={user}',
        f'DJANGO_EMAIL_PORT={port}',
        'DOCKER_CONTAINER=1',
    ]

    with open(django_env_path, 'w') as f:
        f.write('\n'.join(django_config))


def setup_config(_args):
    config = yaml.load(open(CONFIG_PATH), Loader=yaml.FullLoader)
    setup_db(config)
    setup_flower(config)
    setup_rabbitmq(config)
    setup_django(config)


def start(_args):
    command = ['docker-compose'] + get_compose_files() + ['up', '--build', '-d']

    run_command(command, cwd=BASE_DIR)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Control CTForces')
    subparsers = parser.add_subparsers()

    setup_parser = subparsers.add_parser(
        'setup',
        help='Transfer centralized config to environment files'
    )
    setup_parser.set_defaults(func=setup_config)

    start_parser = subparsers.add_parser(
        'start',
        help='Start ctforces'
    )
    start_parser.set_defaults(func=start)

    if os.environ.get('CTFORCES_DEV'):
        DOCKER_COMPOSE_FILES += [os.path.join(BASE_DIR, 'docker-compose.dev.yml')]

    parsed = parser.parse_args()

    try:
        parsed.func(parsed)
    except Exception as e:
        tb = traceback.format_exc()
        print('Got exception:', e, tb)
        exit(1)

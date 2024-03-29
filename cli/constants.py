from pathlib import Path

ADMIN_USER = 'forcad'

BASE_DIR = Path(__file__).absolute().resolve().parents[1]
DEV_COMPOSE_FILE = 'docker-compose.dev.yml'
PROD_COMPOSE_FILE = 'docker-compose.yml'

CONFIG_PATH = BASE_DIR / 'config.yml'

DOCKER_CONFIG_DIR = BASE_DIR / 'configs'
DOCKER_VOLUMES_DIR = BASE_DIR / 'volumes'

ADMIN_ENV_PATH = DOCKER_CONFIG_DIR / 'admin.env'
DJANGO_ENV_PATH = DOCKER_CONFIG_DIR / 'django' / 'environment.env'
S3_ENV_PATH = DOCKER_CONFIG_DIR / 's3.env'
POSTGRES_ENV_PATH = DOCKER_CONFIG_DIR / 'postgres.env'
RABBITMQ_ENV_PATH = DOCKER_CONFIG_DIR / 'rabbitmq.env'

DEFAULT_LOGO = 'https://i.ibb.co/hM3g4yx/E8-B437-F5-BA3-C-4-AE5-9-B4-B-649-AB0-C555-C6.png'

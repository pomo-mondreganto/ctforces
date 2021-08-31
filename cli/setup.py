import secrets

import click

from . import utils, constants, models


@click.command(help='Initialize CTForces configuration')
def setup(**_kwargs):
    config = utils.load_config()
    setup_db(config.db)
    setup_rabbitmq(config.rabbitmq)
    setup_admin_api(config.admin)
    setup_django(config.django)
    setup_s3(config.s3)


def setup_db(config: models.DatabaseConfig):
    postgres_config = [
        "# THIS FILE IS MANAGED BY 'control.py'",
        f'POSTGRES_HOST={config.host}',
        f'POSTGRES_PORT={config.port}',
        f'POSTGRES_USER={config.user}',
        f'POSTGRES_PASSWORD={config.password}',
        f'POSTGRES_DB={config.dbname}',
    ]

    utils.print_bold(f'Writing database env to {constants.POSTGRES_ENV_PATH}')
    constants.POSTGRES_ENV_PATH.write_text('\n'.join(postgres_config))


def setup_rabbitmq(config: models.RabbitMQConfig):
    rabbitmq_config = [
        "# THIS FILE IS MANAGED BY 'control.py'",
        f'RABBITMQ_HOST={config.host}',
        f'RABBITMQ_PORT={config.port}',
        f'RABBITMQ_DEFAULT_USER={config.user}',
        f'RABBITMQ_DEFAULT_PASS={config.password}',
        f'RABBITMQ_DEFAULT_VHOST={config.vhost}',
    ]

    utils.print_bold(f'Writing broker env to {constants.RABBITMQ_ENV_PATH}')
    constants.RABBITMQ_ENV_PATH.write_text('\n'.join(rabbitmq_config))


def setup_admin_api(config: models.AdminConfig):
    admin_config = [
        "# THIS FILE IS MANAGED BY 'control.py'",
        f'ADMIN_USERNAME={config.user}',
        f'ADMIN_PASSWORD={config.password}',
    ]

    utils.print_bold(f'Writing admin env to {constants.ADMIN_ENV_PATH}')
    constants.ADMIN_ENV_PATH.write_text('\n'.join(admin_config))


def setup_django(config: models.DjangoConfig):
    debug = '1' if config.debug else '0'
    secret_key = config.secret_key or secrets.token_hex(32)

    email = config.email
    email_config = [
        f'DJANGO_EMAIL_URL={email.url}',
    ]

    if email.smtp:
        cfg = email.smtp
        email_config += [
            'DJANGO_EMAIL_MODE=smtp',
            f'DJANGO_EMAIL_HOST={cfg.host}',
            f'DJANGO_EMAIL_USER={cfg.user}',
            f'DJANGO_EMAIL_PORT={cfg.port}',
            f'DJANGO_EMAIL_PASSWORD={cfg.password}',
        ]
    elif email.sendgrid:
        cfg = email.sendgrid
        email_config += [
            'DJANGO_EMAIL_MODE=sendgrid',
            f'SENDGRID_API_KEY={cfg.api_key}',
            f'SENDGRID_FROM_EMAIL={cfg.from_email}',
        ]
    else:
        email_config += [
            'DJANGO_EMAIL_MODE=',
        ]

    django_config = [
        "# THIS FILE IS MANAGED BY 'control.py'",
        f'DJANGO_DEBUG={debug}',
        f'DJANGO_SECRET_KEY={secret_key}',
        f'DJANGO_LOGO_LINK={config.logo}',
    ]
    django_config += email_config
    utils.print_bold(f'Writing django env to {constants.DJANGO_ENV_PATH}')
    constants.DJANGO_ENV_PATH.write_text('\n'.join(django_config))


def setup_s3(config: models.S3Config):
    s3_config = [
        "# THIS FILE IS MANAGED BY 'control.py'",
        f'S3_ENDPOINT={config.endpoint}',
        f'S3_ACCESS_KEY={config.access_key}',
        f'S3_SECRET_KEY={config.secret_key}',
        f'S3_BUCKET={config.bucket}',
    ]

    utils.print_bold(f'Writing s3 env to {constants.S3_ENV_PATH}')
    constants.S3_ENV_PATH.write_text('\n'.join(s3_config))

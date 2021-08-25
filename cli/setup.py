import secrets

import click

from . import utils, constants, models, options


@click.command(help='Initialize CTForces configuration')
@options.with_prod_option
def setup(**_kwargs):
    config = utils.load_config()
    setup_db(config.db)
    setup_rabbitmq(config.rabbitmq)
    setup_admin_api(config.admin)
    setup_django(config.django)


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
            f'SENDGRID_USER={cfg.user}',
        ]
    else:
        email_config += [
            'DJANGO_EMAIL_MODE=',
        ]

    django_config = [
        "# THIS FILE IS MANAGED BY 'control.py'",
        f'DJANGO_DEBUG={debug}',
        f'DJANGO_SECRET_KEY={secret_key}',
    ]
    django_config += email_config
    utils.print_bold(f'Writing django env to {constants.DJANGO_ENV_PATH}')
    constants.DJANGO_ENV_PATH.write_text('\n'.join(django_config))
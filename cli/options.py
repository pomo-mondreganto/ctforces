import click


def with_prod_option(func):
    return click.option(
        '--prod',
        is_flag=True,
        help='Run production version',
    )(func)

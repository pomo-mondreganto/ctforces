import click

from .options import with_prod_option
from .utils import run_docker


@click.command(help='Start CTForces')
@with_prod_option
def start(**_kwargs):
    run_docker(['up', '-d'])

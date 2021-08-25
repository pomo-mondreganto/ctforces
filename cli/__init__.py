import click

from .reset import reset
from .setup import setup
from .start import start


@click.group()
def cli():
    pass


cli: click.Group
cli.add_command(reset)
cli.add_command(setup)
cli.add_command(start)

__all__ = ('cli',)

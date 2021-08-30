import click

from . import utils


@click.command(help='Reset the game & clean up')
def reset():
    utils.print_bold('Bringing down services')
    utils.run_docker(['down', '-v'])
    utils.print_success('Done!')

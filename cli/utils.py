import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

import click
import yaml
from pydantic import ValidationError

from . import constants, models


def load_config() -> models.Config:
    print_bold(f'Loading configuration from {constants.CONFIG_PATH}')

    if not constants.CONFIG_PATH.is_file():
        print_error('Config file is missing')
        sys.exit(1)

    with constants.CONFIG_PATH.open() as f:
        raw = yaml.safe_load(f)

    try:
        config = models.Config.parse_obj(raw)
    except ValidationError as e:
        print_error(f'Invalid configuration file: {e}')
        sys.exit(1)

    return config


def run_command(command: List[str], cwd=None, env=None):
    print_bold(f'Running command {command}')
    p = subprocess.Popen(command, cwd=cwd, env=env)
    rc = p.wait()
    if rc != 0:
        print_error(f'Command {command} failed!')
        sys.exit(1)


def get_output(command: List[str], cwd=None, env=None) -> str:
    print_bold(f'Running command {command}')
    return subprocess.check_output(command, cwd=cwd, env=env).decode()


def run_docker(args: List[str]):
    ctx = click.get_current_context()
    prod = ctx.params.get('prod')

    compose = constants.PROD_COMPOSE_FILE if prod else constants.DEV_COMPOSE_FILE
    base = ['docker-compose', '-f', compose]

    run_command(base + args, cwd=constants.BASE_DIR)


def print_file_exception_info(_func, path, _exc_info):
    print_bold(f'File {path} not found')


def print_error(message: str):
    click.secho(message, fg='red', err=True)


def print_success(message: str):
    click.secho(message, fg='green', err=True)


def print_bold(message: str):
    click.secho(message, bold=True, err=True)


def remove_file(path: Path):
    if not path.exists():
        return

    print_bold(f'Removing file {path}')
    if not path.is_file():
        print_error(f'Not a file: {path}')
        return

    try:
        path.unlink()
    except FileNotFoundError:
        pass


def remove_dir(path: Path):
    if not path.exists():
        return

    print_bold(f'Removing directory {path}')
    if not path.is_dir():
        print_error(f'Not a directory: {path}')
        return

    shutil.rmtree(path, ignore_errors=True)

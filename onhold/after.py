from typing import Optional
from sys import exit, stderr
from pathlib import Path
from os import environ

from .base import play_after, dumb_pipe, using_path, \
  play_file, is_pipeline, RC_ENV_VAR, DEFAULT_SOUND, RC_OK

import click


ENV_VAR = 'DING'


def run(file: Path):
  with play_after(file) as path:
    if not is_pipeline():
      return

    dumb_pipe()


@click.command(help="Play specified sound after job is complete.")
@click.option('-s', '--sound_path', required=False,
  type=click.Path(exists=True), help="Path to sound to play.")
@click.option('-i', '--ignore', required=False,
  is_flag=True, default=False, help="Suppress warnings.")
def cmd(sound_path: Optional[str], ignore: bool):
  with using_path(sound_path, ignore, DEFAULT_SOUND, ENV_VAR) as path:
    run(path)


if __name__ == "__main__":
  cmd()

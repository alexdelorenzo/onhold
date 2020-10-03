from typing import Optional
from sys import exit, stderr
from pathlib import Path
from os import environ

from .base import dumb_pipe, using_path, is_pipeline, \
  RC_ENV_VAR, RC_OK

from play_sounds import play_after, DEFAULT_SOUND
import click


ENV_VAR = 'DING'


def run(file: Path):
  with play_after(file):
    if not is_pipeline():
      return

    dumb_pipe()


@click.command(help="Play specified sound after job is complete.")
@click.option('-s', '--sound_path', required=False,
  type=click.Path(exists=True), help="Path to sound to play.")
@click.option('-w', '--warn', required=False,
  is_flag=True, default=False, help="Show warnings.")
def cmd(sound_path: Optional[str], warn: bool):
  with using_path(sound_path, warn, DEFAULT_SOUND, ENV_VAR) as path:
    run(path)


if __name__ == "__main__":
  cmd()

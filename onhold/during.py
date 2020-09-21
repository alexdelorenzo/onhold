from typing import Optional
from sys import exit, stderr
from pathlib import Path
from os import environ

from .base import dumb_pipe, using_path, play_while_running, \
  is_pipeline, RC_ENV_VAR, DEFAULT_SOUND, RC_OK

import click


ENV_VAR = 'ONHOLD'



def run(file: Optional[Path] = None):
  if not file:
    dumb_pipe()
    return 

  with play_while_running(file) as proc:
    dumb_pipe()


@click.command(help="""Play the specified sound file while data is passed in through standard input and passed through standard output.""")
@click.option('-s', '--sound_path', required=False,
  type=click.Path(exists=True), help="Path to sound to play.")
@click.option('-i', '--ignore', required=False,
  is_flag=True, default=False, help="Suppress warnings.")
def cmd(sound_path: Optional[str], ignore: bool):
  with using_path(sound_path, ignore) as path:
    run(path)


if __name__ == "__main__":
  cmd()

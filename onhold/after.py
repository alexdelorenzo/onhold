from os import environ
from pathlib import Path
from sys import exit, stderr

from .base import play_after, dumb_pipe, \
  play_file, RC_ENV_VAR, DEFAULT_SOUND, RC_OK

import click


ENV_VAR = 'DING'


def run(file: Path):
  try:
    dumb_pipe()

  finally:
    if file:
      play_file(file)


@click.command(help="Play specified sound after job is complete.")
@click.option('-s', '--sound_path', required=False,
  type=click.Path(exists=True), help="Path to sound to play.")
@click.option('-i', '--ignore', required=False,
  is_flag=True, default=False, help="Suppress warnings.")
def cmd(sound_path, ignore):
  path: Optional[Path] = DEFAULT_SOUND

  if sound_path:
    path = Path(str(sound_path))

  else:
    if file := environ.get(ENV_VAR):
      path = Path(file)

    elif not ignore:
      stderr.write(f"Please set ${ENV_VAR} or use the -s flag.\n")

  run(path)

  if path:
    exit(RC_OK)
    
  else:
    exit(RC_ENV_VAR)


if __name__ == "__main__":
  cmd()

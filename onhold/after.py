from typing import Optional
from pathlib import Path

from play_sounds import play_after, bell_after, DEFAULT_SOUND
import click

from .base import dumb_pipe, using_path, is_pipeline


ENV_VAR = 'DING'


def run(file: Optional[Path]):
  with play_after(file):
    if not is_pipeline():
      return

    dumb_pipe()


@click.command(help="Play specified sound after shell job is completed.")
@click.option('-s', '--sound_path', required=False,
  type=click.Path(exists=True), help="Path to sound to play.")
@click.option('-b', '--bell', required=False,
  default=False, show_default=True, is_flag=True,
  type=click.BOOL, help="Ring the terminal bell, as well.")
@click.option('-w', '--warn', required=False,
  is_flag=True, default=False, help="Show warnings.")
def cmd(sound_path: Optional[str], bell: bool, warn: bool):
  with bell_after(bell), \
       using_path(sound_path, warn, DEFAULT_SOUND, ENV_VAR) as path:
    run(path)


if __name__ == "__main__":
  cmd()

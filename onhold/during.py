from typing import Optional
from pathlib import Path

from play_sounds import play_while_running, bell_after
import click

from .base import dumb_pipe, using_path


def run(file: Optional[Path] = None):
  if not file:
    dumb_pipe()
    return

  with play_while_running(file):
    dumb_pipe()


@click.command(
  help=(
    "Play the specified sound file while data is passed in "
    "through standard input and passed through standard output."
  )
)
@click.option('-s', '--sound_path', required=False,
  type=click.Path(exists=True), help="Path to sound to play.")
@click.option('-b', '--bell', required=False,
  default=False, show_default=True, is_flag=True,
  type=click.BOOL, help="Ring the terminal bell, as well.")
@click.option('-w', '--warn', required=False,
  is_flag=True, default=False, help="Show warnings.")
def cmd(sound_path: Optional[str], bell: bool, warn: bool):
  with bell_after(bell), \
       using_path(sound_path, warn) as path:
    run(path)


if __name__ == "__main__":
  cmd()

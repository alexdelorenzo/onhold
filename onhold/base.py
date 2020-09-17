from sys import stdin, stdout, exit, stderr
from pathlib import Path
from multiprocessing import Process
from contextlib import contextmanager
from os import environ
from typing import Optional

from playsound import playsound
import click


RC_OK = 0
RC_ENV_VAR = 1
ENV_VAR = 'ONHOLD'


def get_assets_dir() -> Path:
  return Path(__file__).parent / 'assets'


DEFAULT_ASSETS = get_assets_dir()
DEFAULT_SONG = DEFAULT_ASSETS / 'song.mp3'
DEFAULT_SOUND = DEFAULT_ASSETS / 'ding.ogg'


def play_file(file: Path):
  playsound(str(file.absolute()))


def play_loop(file: Path):
  try:
    while True:
      play_file(file)

  except Exception as e:
    stderr.write(f"Error while trying to play {file}: {e}\n")


def play_process(file: Path) -> Process:
  proc = Process(target=play_loop, args=(file,))
  proc.start()

  return proc


def kill_proc(proc: Process):
  proc.kill()
  proc.join()


@contextmanager
def play_while_running(file: Path):
  proc = play_process(file)

  try:
    yield proc

  finally:
    kill_proc(proc)


@contextmanager
def play_after(file: Path):
  yield

  if file:
    play_file(file)


def dumb_pipe():
  for line in stdin.buffer:
    stdout.buffer.write(line)


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
def cmd(sound_path, ignore):
  path: Optional[Path] = DEFAULT_SONG

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

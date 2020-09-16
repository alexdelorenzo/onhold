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


def play_file(file: Path):
  try:
    playsound(str(file.absolute()))

  except Exception as e:
    stderr.write(f"{type(e)}: Could not play {file}.")


def play_loop(file: Path):
  while True:
    play_file(file)


def play_process(file: Path) -> Process:
  proc = Process(target=play_loop, args=(file,))
  proc.start()

  return proc


def kill_and_exit(proc: Process):
  proc.kill()
  proc.join()
  exit(RC_OK)


@contextmanager
def play_while_running(file: Path):
  proc = play_process(file)

  try:
    yield proc

  finally:
    kill_and_exit(proc)


@contextmanager
def play_after(file: Path):
  yield

  if file:
    play_file(file)


def dumb_pipe():
  for line in stdin:
    stdout.write(line)


def run(file: Optional[Path] = None):
  if not file:
    dumb_pipe()
    return 

  with play_while_running(file) as proc:
    dumb_pipe()


@click.command(help="""Play the specified sound file
while data is passed in through standard input and
 passed through standard output.""")
@click.option('-s', '--sound_path', required=False,
  type=click.Path(exists=True))
def cmd(sound_path):
  path: Optional[Path] = None

  if sound_path:
    path = Path(str(sound_path))

  else:
    if ENV_VAR in environ:
      path = Path(file_loc)

    else:
      stderr.write(f"Please set ${ENV_VAR}.\n")

    run(path)

    if not path:
      exit(RC_ENV_VAR)



if __name__ == "__main__":
  cmd()

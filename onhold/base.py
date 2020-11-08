from contextlib import contextmanager, redirect_stdout
from typing import Optional, ContextManager
from sys import stdin, stdout, exit, stderr
from pathlib import Path
from os import environ
import sys
import subprocess

from play_sounds import DEFAULT_SONG
from detect import unix as IS_UNIX
import click


RC_OK = 0
RC_ENV_VAR = 1
ENV_VAR = 'ONHOLD'
BLOCK_WHILE_PLAYING = True


def is_pipeline() -> bool:
  return not stdin.isatty()


def dumb_pipe():
  if IS_UNIX:
    # if we're on unix, just redirect via shell
    subprocess.run(
      "cat",
      shell=True,
      stdin=stdin,
      stdout=stdout
    )

  else:
    # if we're on windows, iterate over stdin
    stdout.buffer.writelines(stdin.buffer)


@contextmanager
def using_path(
  sound_path: Optional[str],
  warn: bool,
  default: Optional[Path] = DEFAULT_SONG,
  env_var: str = ENV_VAR,
) -> ContextManager[Path]:
  path = default

  if sound_path:
    path = Path(str(sound_path))

  elif env_var in environ:
    path = Path(environ[env_var])

  elif warn:
    stderr.write(f"Please set ${env_var} or use the -s flag.\n")

  yield path

  if path:
    exit(RC_OK)

  else:
    exit(RC_ENV_VAR)

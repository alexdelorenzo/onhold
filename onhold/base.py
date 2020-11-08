from contextlib import contextmanager, redirect_stdout
from typing import Optional, ContextManager
from sys import stdin, stdout, exit, stderr
from pathlib import Path
from os import environ
from subprocess import run

from play_sounds import DEFAULT_SONG
from detect import unix as IS_UNIX
import click


RC_OK = 0
RC_ENV_VAR = 1
ENV_VAR = 'ONHOLD'
PIPE_CMD = 'cat'


def is_pipeline() -> bool:
  return not stdin.isatty()


def dumb_pipe():
  if IS_UNIX:
    # if we're on unix, redirect via shell
    run(
      PIPE_CMD,
      shell=True,
      stdin=stdin.buffer,
      stdout=stdout.buffer
    )

  else:
    # if we're some other platform, iterate over stdin
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

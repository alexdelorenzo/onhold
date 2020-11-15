from contextlib import contextmanager
from typing import Optional, ContextManager
from sys import stdin, stdout, stderr, exit
from pathlib import Path
from os import environ
#from subprocess import run

from play_sounds import DEFAULT_SONG


RC_OK = 0
RC_ENV_VAR = 1
ENV_VAR = 'ONHOLD'

KB = 2 ** 10
CHUNK = 64 * KB


def is_pipeline() -> bool:
  return not stdin.isatty()


# python 3.8+ compatible
#def dumb_pipe():
#  while data := stdin.buffer.read(CHUNK):
#    stdout.buffer.write(data)


# python 3.6 compatible
def dumb_pipe():
  while True:
    data = stdin.buffer.read(CHUNK)

    if not data:
      break

    stdout.buffer.write(data)



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

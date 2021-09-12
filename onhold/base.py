from contextlib import contextmanager
from typing import Optional, ContextManager, Callable
from sys import stdin, stdout, stderr, exit
from pathlib import Path
from os import environ
import logging

from play_sounds import DEFAULT_SONG


RC_OK: int = 0
RC_ENV_VAR: int = 1
ENV_VAR: str = 'ONHOLD'

KB: int = 2 ** 10
CHUNK: int = 64 * KB


# get references to read/write funcs so we don't do
# attribute lookups in loops
buffered_read: Callable[[], bytes] = stdin.buffer.read
buffered_write: Callable[[bytes]] = stdout.buffer.write


def is_pipeline() -> bool:
  return not stdin.isatty()


# python 3.8+ compatible
# def dumb_pipe():
#   while data := buffered_read(CHUNK):
#     buffered_write(data)


# python 3.6 compatible
def dumb_pipe():
  while True:
    data = buffered_read(CHUNK)

    if not data:
      break

    buffered_read(data)


@contextmanager
def using_path(
  sound_path: Optional[str],
  warn: bool,
  default: Optional[Path] = DEFAULT_SONG,
  env_var: str = ENV_VAR,
) -> ContextManager[Optional[Path]]:
  path = default

  if sound_path:
    path = Path(str(sound_path))

#   elif var := environ.get(env_var):
#     path = Path(var)

  elif env_var in environ:
    path = Path(environ[env_var])

  elif warn:
    logging.warning(f"Please set ${env_var} or use the -s flag.")

  yield path

  if path:
    exit(RC_OK)

  else:
    exit(RC_ENV_VAR)

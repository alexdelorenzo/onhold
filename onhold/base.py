from typing import Optional, ContextManager
from sys import stdin, stdout, exit, stderr
from pathlib import Path
from contextlib import contextmanager
from os import environ
from platform import platform

from play_sounds import DEFAULT_SONG
import click



RC_OK = 0
RC_ENV_VAR = 1
ENV_VAR = 'ONHOLD'
BLOCK_WHILE_PLAYING = True


#def get_assets_dir() -> Path:
  #return Path(__file__).parent / 'assets'


#DEFAULT_ASSETS = get_assets_dir()
#DEFAULT_SONG = DEFAULT_ASSETS / 'song.mp3'
#DEFAULT_SOUND = DEFAULT_ASSETS / 'ding.ogg'

PLATFORM = platform().lower()


def is_pipeline() -> bool:
  return not stdin.isatty()


def dumb_pipe():
  for line in stdin.buffer:
    stdout.buffer.write(line)
    stdout.buffer.flush()


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

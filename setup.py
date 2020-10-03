__author__ = "Alex DeLorenzo"
from setuptools import setup
from pathlib import Path


NAME = "onhold"
VERSION = "0.3.8"
LICENSE = "AGPL-3.0"

DESC = "🔊 Play music while and after jobs complete"

REQUIREMENTS = \
  Path('requirements.txt') \
    .read_text() \
    .split('\n')

README = Path('README.md').read_text()

ENTRY_POINTS = {
  "console_scripts":
    [f"{NAME} = {NAME}.during:cmd",
      f"ding = {NAME}.after:cmd"]
}

setup(
      name=NAME,
      version=VERSION,
      description=DESC,
      long_description=README,
      long_description_content_type="text/markdown",
      url="https://alexdelorenzo.dev",
      author=__author__,
      license=LICENSE,
      packages=[NAME],
      zip_safe=False,
      install_requires=REQUIREMENTS,
      entry_points=ENTRY_POINTS,
      python_requires='>=3.6',
      include_package_data=True,
      package_data={'onhold': ['assets/*']},
)

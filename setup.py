__author__ = "Alex DeLorenzo"
from setuptools import setup
from pathlib import Path


NAME = "onhold"
VERSION = "0.1.11"
LICENSE = "AGPL-3.0"

requirements = \
  Path('requirements.txt') \
    .read_text() \
    .split('\n')

readme = Path('README.md').read_text()

setup(
      name=NAME,
      version=VERSION,
      description="Play the specified sound file while data is passed in through standard input and passed through standard output.",
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://alexdelorenzo.dev",
      author=__author__,
      license=LICENSE,
      packages=[NAME],
      zip_safe=False,
      install_requires=requirements,
      entry_points={"console_scripts":
                      [f"{NAME} = {NAME}.base:cmd",
                       f"ding = {NAME}.after:cmd"]},
      python_requires='>=3.6',
      include_package_data=True,
      package_data={'onhold': ['assets/*']},
)

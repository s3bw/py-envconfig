from pathlib import PurePath, Path

from setuptools import setup
from setuptools import find_packages


HERE = PurePath(__file__).parent
VERSION_PATH = Path() / HERE / "envconf" / "__version__.py"


about = {}
exec(VERSION_PATH.read_text(), about)


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=["__description__"],
    author="s.williamswynn.mail@gmail.com",
    packages=find_packages(),
)

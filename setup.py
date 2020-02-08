import codecs

from pathlib import PurePath, Path

from setuptools import setup
from setuptools import find_packages


HERE = PurePath(__file__).parent
VERSION_PATH = Path() / HERE / "envconfig" / "__version__.py"


about = {}
with open(VERSION_PATH) as file:
    exec(file.read(), about)

with codecs.open(HERE / "README.md", encoding="utf-8") as file:
    long_description = "\n" + file.read()


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="S. Williams-Wynn",
    author_email="s.williamswynn.mail@gmail.com",
    packages=find_packages(),
    install_requires=about["__dependencies__"],
    python_requires=">=3.6",
)

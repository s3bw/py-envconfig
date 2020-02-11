""" Print python package version from wheel."""
from os import listdir
from pathlib import Path

from wheel_inspect import inspect_wheel

DIST = "./dist/"


def fetch_metadata():
    for file in listdir(DIST):
        if file.endswith(".whl"):
            path = Path(DIST, file)
            return inspect_wheel(path)


def main():
    meta = fetch_metadata()
    return meta["dist_info"]["metadata"]["version"]


if __name__ == "__main__":
    print(main())

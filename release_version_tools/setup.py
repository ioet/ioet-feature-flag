from setuptools import setup, find_packages

__version__ = "0.0.0"

setup(
   name="setup",
   version=__version__,
    packages=(
        find_packages() +
        find_packages(where="./")
    ),
)

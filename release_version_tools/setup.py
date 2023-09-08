from setuptools import setup, find_packages

__version__ = "0.5.1"

setup(
   name="setup",
   version=__version__,
    packages=(
        find_packages() +
        find_packages(where=".c/")
    ),
)

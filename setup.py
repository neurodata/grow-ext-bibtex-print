from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "requirements.txt")) as f:
    required = f.read().splitlines()


setup(
    name="grow-ext-bibtex-print",
    version="0.0.7",
    license="MIT",
    author="Ben Falk",
    author_email="falk.ben@gmail.com",
    include_package_data=False,
    packages=["bibtex_print"],
    install_requires=required,
)

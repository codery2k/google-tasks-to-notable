"""Python setup.py for gtasks_to_txt package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("gtasks_to_txt", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="gtasks_to_txt",
    version=read("gtasks_to_txt", "VERSION"),
    description="Command line tool to convert Google Tasks export to text files",
    url="https://github.com/codery2k/gtasks_to_txt/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="codery2k",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["gtasks_to_txt = gtasks_to_txt.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)

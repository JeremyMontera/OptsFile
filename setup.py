from setuptools import find_packages, setup

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name = "OptsFile",
    version = "0.0.1",
    description = "...",
    long_description = readme,
    author = "Jeremy Montera",
    author_email = "wittkopp.jeremy@gmail.com",
    packages = find_packages(exclude = ("tests", "docs"))
)
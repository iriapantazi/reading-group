from path import Path
from setuptools import find_packages, setup

setup(
    name="reading-group",
    version="0.0.1",
    author="Your Name",
    description="A simple reading group agent",
    packages=find_packages(where=["src"]),
    include_package_data=True,
)

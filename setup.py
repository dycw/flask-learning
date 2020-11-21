from __future__ import annotations

from setuptools import find_packages
from setuptools import setup


setup(
    name="flaskr",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
    ],
)

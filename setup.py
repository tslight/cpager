# Copyright (c) 2018, Toby Slight. All rights reserved.
# ISC License (ISCL) - see LICENSE file for details.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cpager",
    version="0.0.3",
    author="Toby Slight",
    author_email="tslight@pm.me",
    description="Curses Pager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tslight/cpager",
    install_requires=["cansi"],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ),
    entry_points={"console_scripts": ["cpager = cpager.cpager:main"]},
)

#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="ify",
    version="1.0.0",
    description="Text formatting utilities for code and constant generation",
    author="David Taylor",
    author_email="david@cloudartisan.com",
    py_modules=["alignify", "constantify", "wrapify", "testify"],
    entry_points={
        'console_scripts': [
            'alignify=alignify:main',
            'constantify=constantify:main',
            'wrapify=wrapify:main',
            'testify=testify:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
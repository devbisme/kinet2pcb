#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

__author__ = "Dave Vandenbout"
__email__ = "dave@vdb.name"
__version__ = "1.1.2"

if "sdist" in sys.argv[1:]:
    with open("kinet2pcb/pckg_info.py", "w") as f:
        for name in ["__version__", "__author__", "__email__"]:
            f.write("{} = '{}'\n".format(name, locals()[name]))

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "kinparse >= 0.1.2",
    "hierplace",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest",
]

setup(
    author=__author__,
    author_email=__email__,
    version=__version__,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    description="Convert KiCad netlist into a PCBNEW .kicad_pcb file.",
    entry_points={
        "console_scripts": [
            "kinet2pcb=kinet2pcb.kinet2pcb:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="kinet2pcb KiCad EDA PCBNEW SKiDL",
    name="kinet2pcb",
    packages=find_packages(include=["kinet2pcb"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/devbisme/kinet2pcb",
    project_urls={
        "Documentation": "https://devbisme.github.io/kinet2pcb",
        "Source": "https://github.com/devbisme/kinet2pcb",
        "Changelog": "https://github.com/devbisme/kinet2pcb/blob/master/HISTORY.rst",
        "Tracker": "https://github.com/devbisme/kinet2pcb/issues",
    },
    zip_safe=False,
)

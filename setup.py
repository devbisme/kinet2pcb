#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys
from setuptools import setup, find_packages

__author__ = 'XESS Corp.'
__email__ = 'info@xess.com'
__version__ = '0.1.0'

if 'sdist' in sys.argv[1:]:
    with open('kinet2brd/pckg_info.py','w') as f:
        for name in ['__version__','__author__','__email__']:
            f.write("{} = '{}'\n".format(name,locals()[name]))

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 
    "kinparse >= 0.1.2",
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author=__author__,
    author_email=__email__,
    version=__version__,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Convert KiCad netlist into a PCBNEW .kicad_pcb file.",
    entry_points={
        'console_scripts': [
            'kinet2brd=kinet2brd.kinet2brd:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='kinet2brd KiCad EDA PCBNEW SKiDL',
    name='kinet2brd',
    packages=find_packages(include=['kinet2brd']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/xesscorp/kinet2brd',
    zip_safe=False,
)

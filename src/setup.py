#!/usr/bin/env python3

import sys
from distutils import core

from setuptools import find_packages

import chateen

__author__ = 'Jan Vykydal'
__license__ = 'GNU GPL Version 3'

if sys.version_info < (3, 8):
    print('Run in python >= 3.8 please.', file=sys.stderr)
    exit(1)


def setup():
    core.setup(
        name='Chateen',
        version=chateen.__version__,
        license='GNU GENERAL PUBLIC LICENSE Version 3',
        author='Jan Vykydal',
        author_email='john.vykydal@gmail.com',
        packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
        data_files=[
            ('html', ['html/help.html', 'html/about.html']),
            ('img', ['img/chateen.svg'])
        ],
        entry_points={
            'gui_scripts': [
                'Chateen = main.py',
            ],
        }
    )


if __name__ == '__main__':
    setup()

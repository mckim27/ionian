#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# *********************************************************************
# @FILE       setup.py

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import sys
from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
IONIAN_REQUIRED_PYTHON = (3, 5)

PY_YAML_MIN_VERSION = '5.1'
LOG_ZERO_MIN_VERSION = '1.5'
BS4_MIN_VERSION = '4.7'
REQUESTS_MIN_VERSION = '2.21'

# This check and everything above must remain compatible with python 2.X.
##########################################################################
#                               INFO                                     #
#                         Unsupported Python                             #
##########################################################################

if CURRENT_PYTHON < IONIAN_REQUIRED_PYTHON:
    sys.stderr.write("""
    This version of Module requires Python {} {}, but you're trying to
    install it on Python {} {}
    """).format(*(IONIAN_REQUIRED_PYTHON + CURRENT_PYTHON))
    sys.exit(1)

REQUIREMENTS = [
    'pyyaml>={0}'.format(PY_YAML_MIN_VERSION),
    'logzero>={0}'.format(LOG_ZERO_MIN_VERSION),
    'beautifulsoup4>={0}'.format(BS4_MIN_VERSION),
    'requests>={0}'.format(REQUESTS_MIN_VERSION)
]

setup(
    name="Ionian News Crawler",
    # namespace_packages=['google'],
    version="0.1.0",
    python_require='>{}.{}'.format(*IONIAN_REQUIRED_PYTHON),
    author="mckim",
    author_email="bluevoice27@gmail.com",
    description=("News Crawler"),
    package=find_packages(),
    license="Apache License 2.0",
    install_requires=REQUIREMENTS,
    classifiers=[
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Windows',
        'Programming Language :: Python',
        'Programming Language :: 3'
        'Programming Language :: 3.5',
        'Programming Language :: 3.6',
        'Programming Language :: 3 :: only'
    ]
)

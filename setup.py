#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# *********************************************************************
# @FILE       setup.py

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import sys
from setuptools import find_packages, setup
from coverage import __version__, __author__, __author_email__, __description__, __license__, __name__

CURRENT_PYTHON = sys.version_info[:2]
IONIAN_REQUIRED_PYTHON = (3, 5)

PY_YAML_MIN_VERSION = '5.1'
LOG_ZERO_MIN_VERSION = '1.5'
BS4_MIN_VERSION = '4.7'
REQUESTS_MIN_VERSION = '2.21'
BOTO3_MIN_VERSION = '1.9'
KAFKA_PYTHON_MIN_VERSION = '1.4'
URL_LIB3_MIN_VERSION = '1.23'

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
    'requests>={0}'.format(REQUESTS_MIN_VERSION),
    'kafka-python>={0}'.format(KAFKA_PYTHON_MIN_VERSION),
    'boto3>={0}'.format(BOTO3_MIN_VERSION),
    'urllib3<={0}'.format(URL_LIB3_MIN_VERSION)
]

setup(
    name=__name__,
    # namespace_packages=['scale'],
    version=__version__,
    python_require='>{}.{}'.format(*IONIAN_REQUIRED_PYTHON),
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    package=find_packages(),
    license=__license__,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Linux',
        'Programming Language :: Python',
        'Programming Language :: 3'
        'Programming Language :: 3.5',
        'Programming Language :: 3.6',
        'Programming Language :: 3 :: only'
    ]
)

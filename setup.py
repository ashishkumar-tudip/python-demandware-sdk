#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages

import dw
#exec(open('dw/__init__.py').read())

setup(
    name = 'dw',
    version = dw.__version__,
    author = re.sub(r'\s+<.*', r'', dw.__author__),
    author_email = re.sub(r'(^.*<)|(>.*$)', r'', dw.__author__),
    url = dw.__url__,
    download_url = dw.__download_url__,
    license = 'GPL',
    description = ('Python Demandware SDK provides access to the OCAPI services.'),
    long_description = open('README').read(),
    packages = find_packages(),
    data_files = [],
    test_suite = 'nose.collector',
    tests_require = ['nose',],
    keywords = [
        'dw',
        'demandware',
        'commerce',
        'ecommerce',
        'e-commerce',
        'ocaapi',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

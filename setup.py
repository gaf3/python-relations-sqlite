#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name="python-relations-sqlite",
    version="0.6.0",
    package_dir = {'': 'lib'},
    py_modules = [
        'relations_sqlite',
        'relations_sqlite.sql',
        'relations_sqlite.expression',
        'relations_sqlite.criterion',
        'relations_sqlite.criteria',
        'relations_sqlite.clause',
        'relations_sqlite.query',
        'relations_sqlite.ddl',
        'relations_sqlite.column',
        'relations_sqlite.index',
        'relations_sqlite.table'
    ],
    install_requires=[]
)

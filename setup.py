# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyneql',
    version='0.1.0',
    description='A simple sparql wrapper to query named entities in the semantic web',
    long_description=readme,
    author='Valérie Hanoka',
    author_email='valerieh@protonmail.com',
    url='https://github.com/Valerie-Hanoka/PyNeQL',
    license=license,
    setup_requires=['nose'],
    tests_require=['coverage'],
    install_requires=['nose', 'python-coveralls', 'six', 'aenum', 'requests', 'fuzzywuzzy', 'python-dateutil'],
    packages=find_packages(exclude=('tests', 'docs'))
)


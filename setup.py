# -*- coding: utf-8 -*-

# Learn more: https://github.com/TODO

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
    author_email='TODO',
    url='https://github.com/TODO',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyneql',
    version='0.1.0',
    description='A SPARQL wrapper to query named entities in the semantic web',
    long_description=readme,
    author='Valérie Hanoka',
    author_email='valerieh@protonmail.com',
    url='https://github.com/Valerie-Hanoka/PyNeQL',
    license=license,
    setup_requires=['nose'],
    tests_require=['coverage'],
    install_requires=[
        'nose>=1.3.7',
        'python-coveralls>=2.9.1',
        'six>=1.11.0',
        'aenum>=2.1.2',
        'requests>=2.18.4',
        'fuzzywuzzy>=0.16.0',
        'python-dateutil>=2.7.2',
        'future',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Text Processing :: Linguistic"
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6"
    ],
    keywords="SPARQL semantic NLP named entity NER",
    packages=find_packages(exclude=('tests', 'docs'))
)



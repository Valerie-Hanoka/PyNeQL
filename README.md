![PyNeQL](https://github.com/Valerie-Hanoka/PyNeQL/blob/master/illustration.png)


A module for searching Named Entity on SPARQL endpoints
===========================================================

[![Python version](https://img.shields.io/badge/python-2.7-ff69b4.svg)](https://img.shields.io/badge/python-2.7-ff69b4.svg)
[![Build Status](https://travis-ci.org/Valerie-Hanoka/PyNeQL.svg?branch=master)](https://travis-ci.org/Valerie-Hanoka/PyNeQL)
[![Coverage Status](https://coveralls.io/repos/github/Valerie-Hanoka/PyNeQL/badge.svg?branch=master)](https://coveralls.io/github/Valerie-Hanoka/PyNeQL?branch=master)
[![Documentation Status](https://readthedocs.org/projects/pyneql/badge/?version=latest)](http://pyneql.readthedocs.io/en/latest/?badge=latest)               
[![Dev Status](https://img.shields.io/badge/status-development%20%C2%AF%5C__(%E3%83%84)__%2F%C2%AF-lightgrey.svg)](https://img.shields.io/badge/status-development%20%C2%AF%5C__(%E3%83%84)__%2F%C2%AF-lightgrey.svg)

---------------


Linked Data is the global database of the World Wide Web.
One can query those linked databases by sending SPARQL queries to different endpoints.

SPARQL vocabularies are huge and it is sometimes tedious to find how to ask for simple
things as Named Entities.

This module aim to provide a very simple way to query named entities by their name, and retrieve
a maximum of information from different SPARQL endpoints.

You can [read the docs](https://pyneql.readthedocs.io/) here.

Table of Contents
-----------------  

- [Quick Start](#quick-start)
    - [Installation Instructions](#installation-instructions)
    - [Usage](#usage)
        - [Finding a Person](#finding-person)
        - [Finding Anything](#finding-anything)

-----------

## Quick Start
<div id='quick-start'/>


### Installation instructions
<div id='installation-instructions'/>


**Nota bene: For the moment, this module is still under development. 
You do not want to use this in production.**


You can install PyNeQL by cloning the project to your local directory

    git clone https://github.com/Valerie-Hanoka/PyNeQL.git

run `setup.py` 

    python setup.py install


I plan to submit it to PyPI soon.


### Usage
<div id='usage'/>


#### Finding a Person
<div id='finding-person'/>

Looking for [Bell Hooks](https://fr.wikipedia.org/wiki/Bell_hooks) in the Bibliothèque Nationale de France, DBPedia, Wikidata and the French DBPedia:

```python
# -*- coding: utf-8 -*-

from pyneql.ontology.person import Person
from pyneql.utils.endpoints import Endpoint

# Looking for Bell Hooks
endpoints = [Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf]
bell_hooks = Person(first_name="bell", last_name="hooks")
bell_hooks.add_query_endpoints(endpoints)
bell_hooks.query()
```

At the moment, the result is as follow:

```python
# The result of the query contains 15 pieces of information about Bell Hooks.
pprint.pprint(bell_hooks.attributes)
# {
#     u'skos:exactMatch': u'http://data.bnf.fr/ark:/12148/cb12519986q#foaf:Person',
#     u'rdf:type': u'foaf:Person',
#     u'foaf:depiction': set([u'http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg?width=300'
#                            ,
#                            u'https://upload.wikimedia.org/wikipedia/commons/7/7b/Bellhooks.jpg'
#                            ,
#                            u'http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg'
#                            ]),
#     u'foaf:name': u'bell hooks',
#     u'rdagroup2elements:biographicalInformation': u'Essayiste et enseignante. - Militante f\xe9minisme et contre la s\xe9gragation raciale. - Fondatrice, en 2014, du bell hooks Institute, Berea College (Ky., \xc9tats-Unis). - Pseudonyme de Gloria Jean Watkins',
#     u'owl:sameAs': set([u'http://data.bnf.fr/ark:/12148/cb12519986q#foaf:Person'
#                        , u'dbpedia_fr:Bell_hooks',
#                        u'http://viaf.org/viaf/79115934',
#                        u'http://data.bnf.fr/ark:/12148/cb12519986q#about'
#                        ]),
#     u'bnf_onto:firstYear': u'1952',
#     u'foaf:gender': u'female',
#     u'rdagroup2elements:countryAssociatedWithThePerson': u'http://id.loc.gov/vocabulary/countries/xxu',
#     u'rdagroup2elements:fieldOfActivityOfThePerson': set([u'http://dewey.info/class/300/'
#             , u'Sciences sociales. Sociologie']),
#     u'rdagroup2elements:languageOfThePerson': u'http://id.loc.gov/vocabulary/iso639-2/eng',
#     u'foaf:familyName': u'hooks',
#     u'foaf:givenName': u'bell',
#     u'validated': 1,
#     u'foaf:page': u'http://data.bnf.fr/12519986/bell_hooks/',
#     }

# It is possible to find further information about Bell Hooks
bell_hooks.find_more_about()

# person.find_more_about() gives 208 more attribute-keys values about her:
len(bell_hooks.attributes)
# 223
```

##### Language of the query

It is also possible to specify the language of the query, 
and retrieve some information about the person. In this Snippet, we are looking 
for [Vivian Qu](https://en.wikipedia.org/wiki/Vivian_Qu) by her Chinese name:


```python 
from pyneql.ontology.person import Person
from pyneql.utils.endpoints import Endpoint
from pyneql.utils.enum import LanguagesIso6391 as Lang


endpoints = [Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf]
vivian_qu = Person(full_name=u'文晏', query_language=Lang.Chinese)
vivian_qu.add_query_endpoints(endpoints)
vivian_qu.query()

# If is possible to access some important information via dedicated methods

vivian_qu.get_names()
# {u'foaf:givenName': u'Vivian',
#  u'foaf:name': [u'\u6587\u664f', u'Vivian Qu'],
#  u'foaf:surname': u'Qu',
#  u'rdfs:label': [u'\u30f4\u30a3\u30f4\u30a3\u30a2\u30f3\u30fb\u30c1\u30e5\u30a4',
#                  u'\u0641\u064a\u0641\u064a\u0627\u0646 \u062a\u0634\u0648',
#                  u'Vivian Qu',
#                  u'\u6587\u664f'],
#  u'wdt:given_name_(P735)': u'wd:Q650494'}


vivian_qu.get_birth_info()
# {'date': datetime.datetime(1950, 1, 1, 0, 0, tzinfo=tzutc()),
#  'place': u'Beijing, China'}
```


#### Finding Anything
<div id='finding-anything'/>

I plan to develop other classes that will allow safe query of named entites of type 
Location, Books, TimePeriods,...

The class Thing will only be used as a common parent for all other named entities classes. 
As it is not safe to use, I describe it there just for fun.


Looking for [አዲስ አበባ](https://en.wikipedia.org/wiki/Addis_Ababa) in Amharic, on DBPedia:

```python
from pyneql.ontology.thing import Thing
from pyneql.utils.endpoints import Endpoint
from pyneql.utils.enum import LanguagesIso6391 as Lang

addis_abeba = Thing(label=u'አዲስ አበባ', query_language=Lang.Amharic)
addis_abeba.add_query_endpoint(Endpoint.dbpedia)
addis_abeba.query(strict_mode=True)

# It is possible to access information via keyword search
addis_abeba.get_attributes_with_keyword('abel')
# {u'rdfs:label': set([u'Adas Ababa',
#                      u'Addis Ababa',
#                      u'Addis Abeba',
#                      u'Addis-Abeb',
#                      u'Addis-Abeba',
#                      u'Addisz-Abeba',
#                      u'Adis Ababa',
#                      u'Adis Abeba',
#                      u'Adis-Abeba',
#                      u'Adis-Abebo',
#                      u'Adisabeba',
#                      u'Ad\xeds Abeba',
#                      u'Neanthopolis',
#                      u'\u018fddis-\u018fb\u0259b\u0259',
#                      u'\u0391\u03bd\u03c4\u03af\u03c2 \u0391\u03bc\u03c0\u03ad\u03bc\u03c0\u03b1',
#                      u'\u0410\u0434\u0434\u0438\u0441-\u0410\u0431\u0435\u0431\xe6',
#                      u'\u0410\u0434\u0434\u0438\u0441-\u0410\u0431\u0435\u0431\u0430',
#                      u'\u0410\u0434\u0438\u0441 \u0410\u0431\u0435\u0431\u0430',
#                      u'\u0410\u0434\u044b\u0441-\u0410\u0431\u044d\u0431\u0430',
#                      u'\u0413\u043e\u0440\u0430\u0434 \u0410\u0434\u044b\u0441-\u0410\u0431\u0435\u0431\u0430',
#                      u'\u0531\u0564\u056b\u057d \u0531\u0562\u0565\u0562\u0561',
#                      u'\u05d0\u05d3\u05d9\u05e1 \u05d0\u05d1\u05d0\u05d1\u05d0',
#                      u'\u05d0\u05d3\u05d9\u05e1 \u05d0\u05d1\u05d1\u05d4',
#                      u'\u0622\u062f\u06cc\u0633 \u0622\u0628\u0627\u0628\u0627',
#                      u'\u0623\u062f\u064a\u0633 \u0623\u0628\u0627\u0628\u0627',
#                      u'\u0626\u0627\u062f\u06cc\u0633 \u0626\u0627\u0628\u0627\u0628\u0627',
#                      u'\u0627\u062f\u064a\u0633 \u0627\u0628\u0627\u0628\u0627',
#                      u'\u0627\u062f\u06cc\u0633 \u0627\u0628\u0627\u0628\u0627',
#                      u'\u0905\u0926\u093f\u0938 \u0905\u092c\u093e\u092c\u093e',
#                      u'\u0905\u0926\u0940\u0938 \u0905\u092c\u093e\u092c\u093e',
#                      u'\u0986\u09a6\u09cd\u09a6\u09bf\u09b8 \u0986\u09ac\u09be\u09ac\u09be',
#                      u'\u0a06\u0a26\u0a3f\u0a38 \u0a06\u0a2c\u0a2c\u0a3e',
#                      u'\u0b85\u0b9f\u0bbf\u0bb8\u0bcd \u0b85\u0baa\u0bbe\u0baa\u0bbe',
#                      u'\u0c05\u0c26\u0c4d\u0c26\u0c3f\u0c38\u0c4d \u0c05\u0c2c\u0c3e\u0c2c\u0c3e',
#                      u'\u0c85\u0ca1\u0cbf\u0cb8\u0ccd \u0c85\u0cac\u0cbe\u0cac',
#                      u'\u0d05\u0d21\u0d3f\u0d38\u0d4d \u0d05\u0d2c\u0d46\u0d2c',
#                      u'\u0e41\u0e2d\u0e14\u0e14\u0e34\u0e2a\u0e2d\u0e32\u0e1a\u0e32\u0e1a\u0e32',
#                      u'\u0f68\u0f0b\u0f4c\u0f72\u0f0b\u0f66\u0f72\u0f0b\u0f68\u0f0b\u0f56\u0f0b\u0f56\u0f0d',
#                      u'\u1021\u102c\u1012\u1005\u103a \u1021\u102c\u1018\u102c\u1018\u102c\u1019\u103c\u102d\u102f\u1037',
#                      u'\u10d0\u10d3\u10d8\u10e1-\u10d0\u10d1\u10d4\u10d1\u10d0',
#                      u'\u12a0\u12f2\u1235 \u12a0\u1260\u1263',
#                      u'\u30a2\u30c7\u30a3\u30b9\u30a2\u30d9\u30d0',
#                      u'\u4e9a\u7684\u65af\u4e9a\u8d1d\u5df4',
#                      u'\u963f\u8fea\u65af\u963f\u8c9d\u5df4',
#                      u'\uc544\ub514\uc2a4\uc544\ubc14\ubc14']),
#  u'skos:altLabel': set([u'Addis',
#                         u'Finifinee',
#                         u'\u0100dd\u012bs \u0100beb\u0101'])

```





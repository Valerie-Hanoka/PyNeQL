PyNEQL: A module for searching Named Entity on SPARQL endpoints
===============================================================

.. toctree::
   :maxdepth: 3
   :glob:
   :hidden:

   Thing
   Person

   Languages
   Endpoints

   license
   modules



Linked Data is the global database of the World Wide Web. One can query those linked databases by sending SPARQL queries to different endpoints.
SPARQL vocabularies are huge and it is sometimes tedious to find how to ask for simple things as Named Entities.

This module aims to provide a very simple way to query named entities by their name, and retrieve a maximum of information from different SPARQL endpoints.

At the moment, only the type of named entities for which query is available are documented.


.. image:: ../../illustration_delimitante.png
  :width: 900
  :alt: ⚓


Quickstart
-----------------------

A simple Named Entity query using **PyNEQL** might look like that::

    from pyneql.ontology.person import Person
    from pyneql.utils.endpoints import Endpoint
    from pyneql.utils.enum import LanguagesIso6391 as Lang

    person = Person(
        first_name="Bill",
        last_name="Gates",
        endpoints=[Endpoint.wikidata, Endpoint.dbpedia])

    person.query()


Accessing the raw results
**************************

>>> person.attributes
{
 'dbo:almaMater': 'dbpedia:Harvard_University',
 'dbo:birthDate': '1955-10-28',
 'dbo:birthName': 'William Henry Gates III _(@en)',
 'dbo:birthPlace': 'dbpedia:Seattle',
 'dbo:birthYear': '1955',
 'dbo:board': {'dbpedia:Microsoft', 'dbpedia:Berkshire_Hathaway'},
 'dbo:networth': '8.17E10',
 'dbo:parent': {'dbpedia:Mary_Maxwell_Gates', 'dbpedia:William_H._Gates,_Sr.'},
 'dbo:personFunction': 'dbpedia:Bill_Gates__1',
 'dbo:residence': 'dbpedia:Medina,_Washington',
 'dbo:spouse': 'dbpedia:Melinda_Gates',
 'rdfs:label': {'Bill Gates _(@de)',
                'Bill Gates _(@en)',
                'Bill Gates _(@es)',
                'Bill Gates _(@fr)',
                'Bill Gates _(@it)',
                'Bill Gates _(@nl)',
                'Bill Gates _(@pl)',
                'Bill Gates _(@pt)',
                'Гейтс, Билл _(@ru)',
                'بيل غيتس _(@ar)',
                'ビル・ゲイツ _(@ja)',
                '比尔·盖茨 _(@zh)'},
[...]
}

Searching for specific information
************************************

>>> person.get_attributes_with_keyword('[Yy]ears?')
{
 'dbo:activeYearsStartYear': '1975',
 'dbo:birthYear': '1955',
 'dbp:years': {'2009', '2014', '1975', '1996'}
 }


To quickly find the entity's labels by languages, use the class variable `labels_by_languages`:

>>> person.labels_by_languages
{
 'de': ['Bill Gates'],
 'en': ['Bill Gates', 'Bill Gates', 'Bill', 'Gates', 'William Henry Gates III'],
 'es': ['Bill Gates'],
 'fr': ['Bill Gates'],
 'it': ['Bill Gates'],
 'ja': ['ビル・ゲイツ'],
 'nl': ['Bill Gates'],
 'pl': ['Bill Gates'],
 'pt': ['Bill Gates'],
 'ru': ['Гейтс, Билл'],
 'zh': ['比尔·盖茨']}
}

Searching for class-specific specific information
**************************************************

There exists some functions to query class-specific information. For instance for NE of type ``Person``, you can use::

    person.get_gender()
    person.get_names()
    person.get_birth_info()
    person.get_death_info()


Finding more about the Named Entity
************************************

Sometimes, the first result set is not enough to find all the relevant information
about a named entity. There is a function which try to fetch all that can be found:

>>> person.find_more_about()

This function launches another query on the same endpoints using the URIs that are labeled `owl:SameAs` in the first
result set.
The additional results are stored at the same place, in ``person.attributes``.


.. image:: ../../illustration_delimitante.png
  :width: 900
  :alt: ⚓


Named Entities Taxonomy
-----------------------

====================  ============  ========
       Type of Named Entity         Status
----------------------------------  --------
Name                  Inherits
====================  ============  ========
:doc:`Thing`                        **Done**
:doc:`Person`         Thing         **Done**
Creative Work         Thing         *WIP*
Book                  Thing         TODO
Location              Thing         TODO
TemporalInformation   Thing         TODO
====================  ============  ========

.. warning:: As you can see, this module is still under development. I plan to develop
             more functionalities (language handling, endpoints,...),
             NE types (Creative Work, Locations, TimePeriods, Chemicals,...)
             and fix some minor bugs ASAP.
             You are very welcome to contribute to the project on `GitHub <https://github.com/Valerie-Hanoka/PyNeQL>`_.


.. image:: ../../illustration_delimitante.png
  :width: 900
  :alt: ⚓



Queries Options
---------------

Languages
^^^^^^^^^^

It is possible to query in multiple languages. See section :doc:`Languages`.


Endpoints
^^^^^^^^^^

At the moment, only a small number of endpoints are supported. See section :doc:`Endpoints`.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

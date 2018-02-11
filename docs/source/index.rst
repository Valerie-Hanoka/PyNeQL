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

>>> person.attributes
{
dbo:almaMater: ([ "dbpedia:Harvard_University" ]),
dbo:birthName: ([ "William Henry Gates III" ]),
dbo:birthYear: ([ 1955 ]),
dbo:board: ([ "dbpedia:Berkshire_Hathaway","dbpedia:Microsoft" ]),
dbo:networth: ([ "8.17E10" ]),
dbo:parent: ([ "dbpedia:Mary_Maxwell_Gates","dbpedia:William_H._Gates,_Sr." ]),
foaf:surname: ([ "Gates" ]),
http://purl.org/linguistics/gold/hypernym: ([ "dbpedia:Magnate","dbpedia:Frontiersman" ]),
http://purl.org/voc/vrank#hasRank: ([ "nodeID://b27516705","nodeID://b6773534","nodeID://b26111660" ]),
owl:sameAs: ([ "dbpedia:Bill_Gates","dbpedia:Bill_Gates_(frontiersman)","dbpedia:Bill_Gates_(politician)" ]),
skos:exactMatch: ([ "dbpedia:Bill_Gates","dbpedia:Bill_Gates_(frontiersman)","dbpedia:Bill_Gates_(politician)" ]),
[...]
}

Searching for specific information

>>> person.get_attributes_with_keyword('title')
{
    dbo:title: ([ "Technology AdvisorofMicrosoft","Chairmanof theTerraPower","Co-Chairmanof theBill & Melinda Gates Foundation","CEOofCascade Investment","ChairmanofCorbis" ]),
    dbpprop:title: ([ "Chairman of Microsoft","Chief Executive Officer of Microsoft","dbpedia:List_of_billionaires" ])
}

There are some functions to query class-specific information. For instance for NE of type ``Person``, you can use::

    person.get_gender()
    person.get_names()
    person.get_birth_info()
    person.get_death_info()


Sometimes, the first result set is not enough to find all the relevant information
about a named entity. There is a function which try to fetch all that can be found:

>>> person.find_more_about()

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
Book                  Thing         *WIP*
Location              Thing         TODO
TemporalInformation   Thing         TODO
====================  ============  ========

.. warning:: As you can see, this module is still under developpement. I plan to develop
             more functionalities (language handling, endpoints,...),
             NE types (Books, Locations, TimePeriods, Chemicals,...)
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


Restraining the queries
^^^^^^^^^^^^^^^^^^^^^^^^

TODO


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

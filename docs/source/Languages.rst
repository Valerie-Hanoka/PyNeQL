Languages available
=========================================

Currently supported languages are listed in the class ``pyneql.utils.enum.LanguagesIso6391``.

.. image:: ../../illustration_delimitante.png
  :width: 600
  :alt: ⚓

Usage
-----

You can use a language by importing this class and using its correspondance in the enumeration::

    from pyneql.utils.enum import LanguagesIso6391 as Lang
    my_language = Lang.Ukrainian


For instance, if we are looking
for ``Холестерин`` in Ukranian (on DBpedia and Wikidata),
we would instantiate the query as follows:

>>> from pyneql.ontology.thing import Thing
>>> from pyneql.utils.endpoints import Endpoint
>>> from pyneql.utils.enum import LanguagesIso6391 as Lang
>>> molecule = Thing(label="Холестерин", query_language=Lang.Ukrainian)
>>> molecule.add_query_endpoints([Endpoint.dbpedia, Endpoint.wikidata])
>>> molecule.query()
>>> molecule.get_attributes_with_keyword('formula')
{
    p:chemical_formula_(P274): ([ "wds:Q43656-C1909B70-FA48-404A-A692-D76CF70A197B" ]),
    wdt:chemical_formula_(P274): ([ "C₂₇H₄₆O" ])
}


.. image:: ../../illustration_delimitante.png
  :width: 600
  :alt: ⚓

Class details
--------------

.. literalinclude:: ../../pyneql/utils/enum.py
    :linenos:
    :language: python
    :start-after: Enum



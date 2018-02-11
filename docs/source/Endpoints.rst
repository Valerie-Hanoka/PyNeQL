Supported Endpoints
=========================================

.. image:: ../../illustration_delimitante.png
  :width: 600
  :alt: ⚓

Usage
-----


Currently supported Endpoints are listed in the class ``pyneql.utils.endpoints.Endpoint`` (only the uncommented ones).
In order to use them in a query, you just need to import this class::

    from pyneql.utils.endpoints import Endpoint
    my_endpoint = Endpoint.dbpedia
    all_endpoints = [e for e in Endpoint]

For instance, if we want to look
for ``Simone de Beauvoir`` on DBpedia, we would instantiate the query as follows:

>>> beauvoir = Person(full_name="Simone de Beauvoir", endpoints=[Endpoint.dbpedia])

To check what endpoints are activated for a query, just look at the content of the ``endpoints`` instance variable:

>>> beauvoir.endpoints
set([<Endpoint.DEFAULT: u'http://dbpedia.org/sparql'>])

If we want to add other endpoints to that query, two methods can do that:

- For a single endpoint:

  >>> beauvoir.add_query_endpoint(Endpoint.bnf)
  >>> beauvoir.endpoints
  set([<Endpoint.DEFAULT: u'http://dbpedia.org/sparql'>, <Endpoint.bnf: u'http://data.bnf.fr/sparql'>])

- For a list of endpoints:

  >>> beauvoir.add_query_endpoints([Endpoint.dbpedia_fr, Endpoint.wikidata])
  >>> beauvoir.endpoints
  set([<Endpoint.DEFAULT: u'http://dbpedia.org/sparql'>, <Endpoint.wikidata: u'https://query.wikidata.org/sparql'>, <Endpoint.dbpedia_fr: u'http://fr.dbpedia.org/sparql'>, <Endpoint.bnf: u'http://data.bnf.fr/sparql'>])

.. image:: ../../illustration_delimitante.png
  :width: 600
  :alt: ⚓

Class details
--------------

.. literalinclude:: ../../pyneql/utils/endpoints.py
    :linenos:
    :language: python
    :start-after: Enum
    :end-before: def



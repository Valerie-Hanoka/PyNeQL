PyNeQL: a module for searching Named Entity on SPARQL endpoints
===========================================================

*In development*
---------------

![alt text](https://github.com/Valerie-Hanoka/PyNeQL/blob/master/illustration.png)


Linked Data is the global database of the World Wide Web.
One can query those linked databases by sending SPARQL queries to different endpoints.

SPARQL vocabularies are huge and it is sometimes tedious to find how to ask for simple
things as Named Entities.

This module aims to provide a very simple way to query named entities by their name, and retrieve
a maximum of information from different SPARQL endpoints.

Installation
-----------

Not yet


Usage
-----

Looking for "Marguerite Duras" in the Bibliothèque Nationale de France and French DBPedia:

.. code:: python

    >>> from personquerybuilder import PersonQuery
    >>> from enum import Endpoint
    >>> from pprint import pprint

    >>> duras = PersonQuery(first_name="Marguerite", last_name="Duras")
    >>> duras.add_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr])
    >>> duras.query()


Ath the moment, the result is as follow:

.. code:: python

    >>> pprint(duras.attributes)
        {u'22-rdf-syntax-ns#type': set([u'http://xmlns.com/foaf/0.1/Person']),
         u'biographicalInformation': set([u'Romanci\xe8re, cin\xe9aste et dramaturge. - Pseudonyme de Marguerite Donnadieu']),
         u'birth': set([u'1914-04-04']),
         u'birthday': set([u'04-04']),
         u'countryAssociatedWithThePerson': set([u'http://id.loc.gov/vocabulary/countries/fr']),
         u'dateOfBirth': set([u'http://data.bnf.fr/date/1914/']),
         u'dateOfDeath': set([u'http://data.bnf.fr/date/1996/']),
         u'death': set([u'1996-03-03']),
         u'depiction': set([u'http://commons.wikimedia.org/wiki/Special:FilePath/Marguerite_Duras_1993.jpg',
                            u'http://commons.wikimedia.org/wiki/Special:FilePath/Marguerite_Duras_1993.jpg?width=300',
                            u'http://gallica.bnf.fr/ark:/12148/bpt6k3323544p.thumbnail',
                            u'http://gallica.bnf.fr/ark:/12148/bpt6k33468995.thumbnail',
                            u'http://gallica.bnf.fr/ark:/12148/bpt6k48048066.thumbnail',
                            u'https://upload.wikimedia.org/wikipedia/commons/e/e9/Marguerite_Duras.png']),
         u'familyName': set([u'Duras']),
         u'fieldOfActivityOfThePerson': set([u'Audiovisuel',
                                             u'Litt\xe9ratures',
                                             u'http://dewey.info/class/791/',
                                             u'http://dewey.info/class/800/']),
         u'firstYear': set([u'1914']),
         u'gender': set([u'female']),
         u'givenName': set([u'Marguerite']),
         u'languageOfThePerson': set([u'http://id.loc.gov/vocabulary/iso639-2/fre']),
         u'lastYear': set([u'1996']),
         u'name': set([u'Marguerite Duras']),
         u'owl#sameAs': set([u'http://data.bnf.fr/ark:/12148/cb119013498#about',
                             u'http://fr.dbpedia.org/resource/Marguerite_Duras',
                             u'http://viaf.org/viaf/97785734',
                             u'http://www.idref.fr/027405168/id']),
         u'page': set([u'http://data.bnf.fr/11901349/marguerite_duras/']),
         u'placeOfBirth': set([u'Gia Dinh (Vietnam)']),
         u'placeOfDeath': set([u'Paris'])}



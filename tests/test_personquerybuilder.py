#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_personquerybuilder is part of the project PyNeQL
Author: Valérie Hanoka

"""
from pyneql.person import Person
from pyneql.enum import (
    Endpoint,
    LanguagesIso6391 as Lang
)

def test_genericsparqlquery_base_case():
    """Person - Base case, no issues: Should pass"""

    duras = Person(first_name="Marguerite", last_name="Duras", query_language=Lang.French)
    duras.add_query_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr])  # Endpoint.dbpedia, Endpoint.dbpedia_fr
    duras.query()

    expected ={
        u'bio:birth': u'1914-04-04',
        u'bio:death': u'1996-03-03',
        u'bnf_onto:firstYear': u'1914',
        u'bnf_onto:lastYear': u'1996',
        u'foaf:birthday': u'04-04',
        u'foaf:depiction': set([u'http://commons.wikimedia.org/wiki/Special:FilePath/Marguerite_Duras_1993.jpg',
                                u'http://commons.wikimedia.org/wiki/Special:FilePath/Marguerite_Duras_1993.jpg?width=300',
                                u'http://gallica.bnf.fr/ark:/12148/bpt6k3323544p.thumbnail',
                                u'http://gallica.bnf.fr/ark:/12148/bpt6k33468995.thumbnail',
                                u'http://gallica.bnf.fr/ark:/12148/bpt6k48048066.thumbnail',
                                u'https://upload.wikimedia.org/wikipedia/commons/e/e9/Marguerite_Duras.png']),
        u'foaf:familyName': u'Duras',
        u'foaf:gender': u'female',
        u'foaf:givenName': u'Marguerite',
        u'foaf:name': u'Marguerite Duras',
        u'foaf:page': u'http://data.bnf.fr/11901349/marguerite_duras/',
        u'owl:sameAs': set([u'dbpedia_fr:Marguerite_Duras',
                            u'http://data.bnf.fr/ark:/12148/cb119013498#about',
                            u'http://data.bnf.fr/ark:/12148/cb119013498#foaf:Person',
                            u'http://viaf.org/viaf/97785734',
                            u'http://www.idref.fr/027405168/id']),
        u'rdagroup2elements:biographicalInformation': u'Romanci\xe8re, cin\xe9aste et dramaturge. - Pseudonyme de Marguerite Donnadieu',
        u'rdagroup2elements:countryAssociatedWithThePerson': u'http://id.loc.gov/vocabulary/countries/fr',
        u'rdagroup2elements:dateOfBirth': u'http://data.bnf.fr/date/1914/',
        u'rdagroup2elements:dateOfDeath': u'http://data.bnf.fr/date/1996/',
        u'rdagroup2elements:fieldOfActivityOfThePerson': set([u'Audiovisuel',
                                                              u'Litt\xe9ratures',
                                                              u'http://dewey.info/class/791/',
                                                              u'http://dewey.info/class/800/']),
        u'rdagroup2elements:languageOfThePerson': u'http://id.loc.gov/vocabulary/iso639-2/fre',
        u'rdagroup2elements:placeOfBirth': u'Gia Dinh (Vietnam)',
        u'rdagroup2elements:placeOfDeath': u'Paris',
        u'rdf:type': u'foaf:Person',
        u'validated': 1}

    assert duras.attributes == expected
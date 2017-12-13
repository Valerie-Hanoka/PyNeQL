#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_personquerybuilder is part of the project PyNeQL
Author: Valérie Hanoka

"""
from pyneql.personquerybuilder import PersonQuery
from pyneql.enum import Endpoint

def test_genericsparqlquery_base_case():
    """PersonQuery - Base case, no issues: Should pass"""

    duras = PersonQuery(first_name="Marguerite", last_name="Duras")
    duras.add_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr])  # Endpoint.dbpedia, Endpoint.dbpedia_fr
    duras.query()

    expected ={
        u'http://data.bnf.fr/ontology/bnf-onto/firstYear': u'1914',
        u'http://data.bnf.fr/ontology/bnf-onto/lastYear': u'1996',
        u'http://rdvocab.info/ElementsGr2/biographicalInformation': u'Romanci\xe8re, cin\xe9aste et dramaturge. - Pseudonyme de Marguerite Donnadieu',
        u'http://rdvocab.info/ElementsGr2/countryAssociatedWithThePerson': u'http://id.loc.gov/vocabulary/countries/fr',
        u'http://rdvocab.info/ElementsGr2/dateOfBirth': u'http://data.bnf.fr/date/1914/',
        u'http://rdvocab.info/ElementsGr2/dateOfDeath': u'http://data.bnf.fr/date/1996/',
        u'http://rdvocab.info/ElementsGr2/fieldOfActivityOfThePerson': set([u'Audiovisuel',
                                                                            u'Litt\xe9ratures',
                                                                            u'http://dewey.info/class/791/',
                                                                            u'http://dewey.info/class/800/']),
        u'http://rdvocab.info/ElementsGr2/languageOfThePerson': u'http://id.loc.gov/vocabulary/iso639-2/fre',
        u'http://rdvocab.info/ElementsGr2/placeOfBirth': u'Gia Dinh (Vietnam)',
        u'http://rdvocab.info/ElementsGr2/placeOfDeath': u'Paris',
        u'http://vocab.org/bio/0.1/birth': u'1914-04-04',
        u'http://vocab.org/bio/0.1/death': u'1996-03-03',
        u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type': u'http://xmlns.com/foaf/0.1/Person',
        u'http://www.w3.org/2002/07/owl#sameAs': set([u'http://data.bnf.fr/ark:/12148/cb119013498#about',
                                                      u'http://fr.dbpedia.org/resource/Marguerite_Duras',
                                                      u'http://viaf.org/viaf/97785734',
                                                      u'http://www.idref.fr/027405168/id']),
        u'http://xmlns.com/foaf/0.1/birthday': u'04-04',
        u'http://xmlns.com/foaf/0.1/depiction': set([u'http://commons.wikimedia.org/wiki/Special:FilePath/Marguerite_Duras_1993.jpg',
                                                     u'http://commons.wikimedia.org/wiki/Special:FilePath/Marguerite_Duras_1993.jpg?width=300',
                                                     u'http://gallica.bnf.fr/ark:/12148/bpt6k3323544p.thumbnail',
                                                     u'http://gallica.bnf.fr/ark:/12148/bpt6k33468995.thumbnail',
                                                     u'http://gallica.bnf.fr/ark:/12148/bpt6k48048066.thumbnail',
                                                     u'https://upload.wikimedia.org/wikipedia/commons/e/e9/Marguerite_Duras.png']),
        u'http://xmlns.com/foaf/0.1/familyName': u'Duras',
        u'http://xmlns.com/foaf/0.1/gender': u'female',
        u'http://xmlns.com/foaf/0.1/givenName': u'Marguerite',
        u'http://xmlns.com/foaf/0.1/name': u'Marguerite Duras',
        u'http://xmlns.com/foaf/0.1/page': u'http://data.bnf.fr/11901349/marguerite_duras/'}

    assert duras.results==expected
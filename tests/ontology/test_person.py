#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import *

from pyneql.ontology.person import Person
from pyneql.utils.enum import LanguagesIso6391 as Lang
from pyneql.utils.endpoints import Endpoint

from pyneql.utils.utils import QueryException

import datetime

# TODO: • test for each the search with first and last name independently
# TODO: • Find why wikidata is not working anymore

##################################################
#                 QUERY
##################################################

@raises(QueryException)
def test_person_incomplete():
    """Person - Not enough arguments: Should fail"""
    Person(first_name="Marguerite", query_language=Lang.French)


# Testing Endpoint: dbpedia
def test_person_dbpedia_query_strict_True():
    """Person - dbpedia - strict=True - : Should pass"""
    person = Person(full_name="Victor Hugo", query_language=Lang.French)
    person.add_query_endpoint(Endpoint.dbpedia)
    person.query(strict_mode=True)

    assert person.get_external_ids() == {
        u'Deutschen_Nationalbibliothek': u'http://d-nb.info/gnd/118554654',
        u'viaf': u'http://viaf.org/viaf/9847974'
    }

def test_person_dbpedia_query_strict_False():
    """Person - dbpedia - strict=False - : Should pass """
    person = Person(full_name="Nan Goldin", query_language=Lang.German)
    person.add_query_endpoint(Endpoint.dbpedia)
    person.query_builder.set_limit(666)
    person.query(strict_mode=False)
    assert u'http://wikidata.dbpedia.org/resource/Q234279' in person.attributes.get(u'owl:sameAs')

# Testing Endpoint: dbpedia_fr

def test_person_dbpedia_fr_query_strict_True():
    """Person - dbpedia_fr - strict=True - : Should pass """
    person = Person(full_name="Jean-Jacques Servan-Schreiber", query_language=Lang.French)
    person.add_query_endpoint(Endpoint.dbpedia_fr)
    person.query(strict_mode=True)
    assert u'freebase:m.05rj1c' in person.attributes.get(u'owl:sameAs')


def test_person_dbpedia_fr_query_strict_False():
    """Person - dbpedia_fr - strict=False - : Should pass """
    person = Person(full_name=u"Hercule Poirot", query_language=Lang.French)
    person.add_query_endpoint(Endpoint.dbpedia_fr)
    person.query(strict_mode=False)
    assert u'freebase:m.0ljm' in person.attributes.get(u'owl:sameAs')


# Testing Endpoint: wikidata
# def test_person_wikidata_query_strict_True():
#     """Person - wikidata - strict=True - : Should pass """
#     person = Person(full_name=u'文晏', query_language=Lang.Chinese)
#     person.add_query_endpoint(Endpoint.wikidata)
#     person.query(strict_mode=True)
#     assert u'wd:Q17025364' in person.attributes.get(u'owl:sameAs')
#
#
# def test_person_wikidata_query_strict_False():
#     """Person - wikidata - strict=False - : Should pass"""
#     person = Person(has_full_name=u"Πλάτωνας", query_language=Lang.Greek_modern)
#     person.add_query_endpoint(Endpoint.wikidata)
#     person.query(strict_mode=False)
#      assert u'wd:Q859' in person.attributes.get(u'owl:sameAs')


# Testing Endpoint: bnf
def test_person_bnf_query_strict_True():
    """Person - bnf - strict=True - : Should pass """
    person = Person(full_name="Simone de Beauvoir", query_language=Lang.French)
    person.add_query_endpoint(Endpoint.bnf)
    person.query(strict_mode=True)
    assert u'dbpedia_fr:Simone_de_Beauvoir' in person.attributes.get(u'owl:sameAs')

def test_person_bnf_query_strict_False():
    """Person - bnf - strict=False - : Should pass """
    person = Person(full_name="Hannah Arendt", query_language=Lang.French)
    person.add_query_endpoint(Endpoint.bnf)
    person.query(strict_mode=False)
    import pprint; pprint.pprint(person.attributes)
    assert u'dbpedia_fr:Hannah_Arendt' in person.attributes.get(u'owl:sameAs')

# With URL

def test_thing_query_URL():
    """Person - URL query - : Should pass """
    person = Person(url='http://data.bnf.fr/ark:/12148/cb118905823#foaf:Person')
    person.add_query_endpoints([Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf])
    person.query(strict_mode=True)
    assert u'http://viaf.org/viaf/17218730' in person.attributes.get(u'owl:sameAs')


##################################################
#                 OTHER METHODS
##################################################


def test_person_deepen_search():
    """Person - find_more_about(): Should pass"""
    endpoints = [Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf]
    joeystarr = Person(full_name=u'Didier Morville', query_language=Lang.French)
    joeystarr.add_query_endpoints(endpoints)
    joeystarr.query(strict_mode=True)
    attr_before_deep_search = len(joeystarr.attributes)
    joeystarr.find_more_about()
    attr_after_deep_search = len(joeystarr.attributes)
    assert attr_before_deep_search < attr_after_deep_search


def test_person_get_death_info():
    """Person - get_death_info : Should pass """
    person = Person(full_name=u'Marguerite Duras', query_language=Lang.French)
    person.add_query_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr, Endpoint.dbpedia])
    person.query(strict_mode=False)


    expected_death = {
        'date': datetime.datetime(1996, 3, 3, 0, 0),
        'other': set([u'1996-03-03+02:00', u'http://data.bnf.fr/date/1996/']),
        'place': set([u'Paris',
                      u'Paris, France',
                      u'dbpedia:Paris',
                      u'dbpedia_fr:6e_arrondissement_de_Paris'
                      ])
    }
    assert person.get_death_info() == expected_death

def test_person_get_birth_info():
    """Person - get_birth_info: Should pass """
    person = Person(last_name="Arendt", first_name="Hannah")
    person.add_query_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr, Endpoint.dbpedia])
    person.query(strict_mode=False)
    import pprint; pprint.pprint(person.get_birth_info())
    expected_birth = {
        'date': datetime.datetime(1906, 10, 14, 0, 0),
        'other': u'http://data.bnf.fr/date/1906/',
        'place': set([u'Hanovre (Allemagne)',
                      u'dbpedia:German_Empire',
                      u'dbpedia:Germany',
                      u'dbpedia:Hanover',
                      u'dbpedia:Linden-Limmer'])
    }
    assert person.get_birth_info() == expected_birth

def test_person_get_gender():
    """Person - get_gender : Should pass """
    person = Person(full_name="Chelsea Manning", query_language=Lang.English)
    person.add_query_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr, Endpoint.dbpedia])
    person.query(strict_mode=False)
    assert person.get_gender() == 'F'

def test_person_get_names():
    """Person - get_names : Should pass """
    person = Person(full_name="RuPaul")
    person.add_query_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr, Endpoint.dbpedia])
    person.query(strict_mode=True)
    names = person.get_names()
    assert u'RuPaul Andre Charles' in names.get(u'dbo:birthName')

def test_person_get_external_ids():
    """Person - : Should pass """
    person = Person(full_name='Virginia Woolf', query_language=Lang.French)
    person.add_query_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr, Endpoint.dbpedia])
    person.query(strict_mode=True)
    result = person.get_external_ids()
    assert u'http://www.idref.fr/027199746/id' in result.get(u'idref')

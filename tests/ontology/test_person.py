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

    assert "Victor Marie Hugo _(@en)" in person.get_attributes_with_keyword('dbo:birthName').values()


def test_person_dbpedia_query_strict_False():
    """Person - dbpedia - strict=False - : Should pass """
    person = Person(full_name="Nan Goldin", query_language=Lang.German)
    person.add_query_endpoint(Endpoint.dbpedia)
    person.query(strict_mode=False)

    is_ok = False
    for ok in ['Q234279' in attr for attr in person.attributes.get(u'owl:sameAs')]:
        is_ok = is_ok or ok

# Testing Endpoint: dbpedia_fr

def test_person_dbpedia_fr_query_strict_True():
    """Person - dbpedia_fr - strict=True - : Should pass """
    full_name = "Jean-Jacques Servan-Schreiber"
    person = Person(full_name=full_name, query_language=Lang.French)
    person.add_query_endpoint(Endpoint.dbpedia_fr)
    person.query(strict_mode=True)

    names = person.attributes.get(u'foaf:name')
    is_ok = False
    if isinstance(names, set):
        is_ok = reduce((lambda x, y: x or y), [full_name in attr for attr in person.attributes.get(u'foaf:name')])
    else:
        is_ok = full_name in names
    assert is_ok


def test_person_dbpedia_fr_query_strict_False():
    """Person - dbpedia_fr - strict=False - : Should pass """
    full_name = u"Hercule Poirot"
    person = Person(full_name=full_name, query_language=Lang.French, endpoints=[Endpoint.dbpedia_fr])
    person.query(strict_mode=False)

    names = person.attributes.get(u'foaf:name')
    is_ok = False
    if isinstance(names, set):
        is_ok = False
        for has_full_name in [full_name in attr for attr in person.attributes.get(u'foaf:name')]:
            is_ok = is_ok or has_full_name
    else:
        is_ok = full_name in names

    assert is_ok


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
    full_name = "Simone de Beauvoir"
    person = Person(full_name=full_name, query_language=Lang.French)
    person.add_query_endpoint(Endpoint.bnf)
    person.query(strict_mode=True)

    names = person.attributes.get(u'foaf:name')
    is_ok = False
    if isinstance(names, set):
        is_ok = reduce((lambda x, y: x or y), [full_name in attr for attr in person.attributes.get(u'foaf:name')])
    else:
        is_ok = full_name in names
    assert is_ok

def test_person_bnf_query_strict_False():
    """Person - bnf - strict=False - : Should pass """
    full_name = "Hannah Arendt"
    person = Person(full_name=full_name, query_language=Lang.French)
    person.add_query_endpoint(Endpoint.bnf)
    person.query(strict_mode=False)
    names = person.attributes.get(u'foaf:name')
    is_ok = False
    if isinstance(names, set):
        is_ok = reduce((lambda x, y: x or y), [full_name in attr for attr in person.attributes.get(u'foaf:name')])
    else:
        is_ok = full_name in names
    assert is_ok

# With URL

def test_thing_query_URL():
    """Person - URL query - : Should pass """
    person = Person(url='http://dbpedia.org/resource/Charles_Baudelaire')
    person.add_query_endpoints([Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf])
    person.query(strict_mode=True)
    assert u'http://dbpedia.org/resource/Charles_Baudelaire' in person.attributes.get(u'owl:sameAs')

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
    assert len(person.get_death_info()) > 0

def test_person_get_birth_info():
    """Person - get_birth_info: Should pass """
    person = Person(last_name="Arendt", first_name="Hannah")
    person.add_query_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr, Endpoint.dbpedia])
    person.query(strict_mode=False)
    assert len(person.get_birth_info()) > 0

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
    assert u'RuPaul Andre Charles _(@en)' in names.get(u'dbo:birthName')

def test_person_get_external_ids():
    """Person - get_external_ids: Should pass """
    person = Person(full_name='Virginia Woolf', query_language=Lang.French)
    person.add_query_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr, Endpoint.dbpedia])
    person.query(strict_mode=True)
    result = person.get_external_ids()
    assert len(result) > 0

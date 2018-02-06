#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_thing.py is part of the project PyNeQL
Author: Valérie Hanoka

"""


from nose.tools import *

from pyneql.ontology.thing import Thing
from pyneql.utils.enum import LanguagesIso6391 as Lang
from pyneql.utils.endpoints import Endpoint
from fuzzywuzzy import fuzz
from pyneql.utils.utils import QueryException

##################################################
#                 QUERY
##################################################

# Testing Endpoint: dbpedia
def test_thing_dbpedia_query_strict_True():
    """Thing - dbpedia - strict=True - : Should pass"""
    thing = Thing(label=u'አዲስ አበባ', query_language=Lang.Amharic)
    thing.add_query_endpoint(Endpoint.dbpedia)
    thing.query(strict_mode=True)

    expected = {
        'args': {
            'object': u'?obj',
            'predicate': u'?pred',
            'subject': u'?Thing'
        },
        'class_name': u'Thing',
        'endpoints': set([Endpoint.dbpedia]),
        'has_label': u'\u12a0\u12f2\u1235 \u12a0\u1260\u1263',
        'query_language': Lang.Amharic,
    }
    assert thing.args == expected.get('args')
    assert thing.class_name == expected.get('class_name')
    assert thing.endpoints == expected.get('endpoints')
    assert thing.has_label == expected.get('has_label')
    assert thing.query_language == expected.get('query_language')
    assert thing.attributes.get(u'owl:sameAs') == u'wd:Q3624'  # https://www.wikidata.org/wiki/Q3624

def test_thing_dbpedia_query_strict_False():
    """Thing - dbpedia - strict=False - : Should pass """
    thing = Thing(label=u"K'iche'-Sprache", query_language=Lang.German)
    thing.add_query_endpoint(Endpoint.dbpedia)
    thing.query_builder.set_limit(666)
    thing.query(strict_mode=False)

    expected ={
        'endpoints': set([Endpoint.dbpedia]),
        'has_label': u"K'iche'-Sprache",
        'query_language': Lang.German,
    }
    assert thing.endpoints == expected.get('endpoints')
    assert thing.has_label == expected.get('has_label')
    assert thing.query_language == expected.get('query_language')
    assert thing.attributes.get(u'owl:sameAs') == u'wd:Q36494'  # https://www.wikidata.org/wiki/Q36494

# Testing Endpoint: dbpedia_fr

def test_thing_dbpedia_fr_query_strict_True():
    """Thing - dbpedia_fr - strict=True - : Should pass """
    thing = Thing(label="Acide pinique", query_language=Lang.French)
    thing.add_query_endpoint(Endpoint.dbpedia_fr)
    thing.query(strict_mode=True)

    assert thing.endpoints == set([Endpoint.dbpedia_fr])
    assert thing.has_label == u'Acide pinique'
    assert thing.query_language == Lang.French
    assert thing.attributes.get(u'dbo:wikiPageID') == u'2849482'


def test_thing_dbpedia_fr_query_strict_False():
    """Thing - dbpedia_fr - strict=False - : Should pass """
    thing = Thing(label=u"11e régiment du génie", query_language=Lang.French)
    thing.add_query_endpoint(Endpoint.dbpedia_fr)
    thing.query(strict_mode=False)

    assert thing.endpoints == set([Endpoint.dbpedia_fr])
    assert thing.has_label == u'11e r\xe9giment du g\xe9nie'
    assert thing.query_language == Lang.French
    assert thing.attributes.get(u'dbo:wikiPageID') == u'2808198'


# Testing Endpoint: wikidata

def test_thing_wikidata_query_strict_True():
    """Thing - wikidata - strict=True - : Should pass """
    thing = Thing()
    thing.add_query_endpoint(Endpoint.wikidata)
    thing.query(strict_mode=True)

    assert thing.endpoints == set([Endpoint.wikidata])
    assert thing.query_language == Lang.English

    expected_query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX wd: <http://www.wikidata.org/entity/> 
    PREFIX schemaorg: <http://schema.org/> 
    PREFIX dbo: <http://dbpedia.org/ontology/> 
    PREFIX wdt_o: <http://www.wikidata.org/ontology#> 
    SELECT DISTINCT ?Thing ?pred ?obj WHERE { 
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } 
    ?Thing ?pred ?obj . 
    { ?Thing a owl:Class  } UNION 
    { ?Thing a schemaorg:Class  } UNION 
    { ?Thing a wd:Q35120  } UNION 
    { ?Thing a schemaorg:Thing  } UNION 
    { ?Thing a wdt_o:Item  } UNION 
    { ?Thing a dbo:Thing  } UNION 
    { ?Thing a owl:Thing  } .  
    } LIMIT 1500
    """
    ratio = fuzz.token_sort_ratio(thing.query_builder.queries[Endpoint.wikidata], expected_query)
    assert ratio == 100


def test_thing_wikidata_query_strict_False():
    """Thing - wikidata - strict=False - : Should pass"""
    thing = Thing(label=u"혁kστ혁ηjh혁kي혁ةsjdジアh", query_language=Lang.DEFAULT)
    thing.add_query_endpoint(Endpoint.wikidata)
    thing.query(strict_mode=False)

    assert thing.endpoints == set([Endpoint.wikidata])
    assert thing.has_label == u'혁kστ혁ηjh혁kي혁ةsjdジアh'
    assert thing.query_language == Lang.English


    expected_query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#> 
    PREFIX wd: <http://www.wikidata.org/entity/> 
    PREFIX schemaorg: <http://schema.org/> 
    PREFIX wdt_o: <http://www.wikidata.org/ontology#> 
    PREFIX dbo: <http://dbpedia.org/ontology/> 
    SELECT DISTINCT ?Thing ?pred ?obj WHERE 
    { SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } 
    ?Thing ?has_label "혁kστ혁ηjh혁kي혁ةsjd@en .
     ?Thing ?pred ?obj .
      { ?Thing a schemaorg:Class  } UNION { ?Thing a owl:Thing  } UNION 
      { ?Thing a schemaorg:Thing  } UNION { ?Thing a wd:Q35120  } UNION 
      { ?Thing a owl:Class  } UNION { ?Thing a dbo:Thing  } UNION { ?Thing a wdt_o:Item  } .  
      } LIMIT 1500
    """
    ratio = fuzz.token_sort_ratio(thing.query_builder.queries[Endpoint.wikidata], expected_query)
    assert ratio == 100


# Testing Endpoint: bnf
def test_thing_bnf_query_strict_True():
    """Thing - bnf - strict=True - : Should pass """
    thing = Thing(label="Thing", query_language=Lang.English)
    thing.add_query_endpoint(Endpoint.bnf)
    thing.query(strict_mode=True)
    assert thing.attributes.get(u'owl:sameAs') == u'owl:Thing'

def test_thing_bnf_query_strict_False():
    """Thing - bnf - strict=False - : Should pass """
    thing = Thing(label="Nothing", query_language=Lang.English)
    thing.add_query_endpoint(Endpoint.bnf)
    thing.query(strict_mode=False)
    assert thing.attributes.get(u'owl:complementOf') == u'owl:Thing'

# With URL

def test_thing_query_URL():
    """Thing - URL query - : Should pass """
    thing = Thing(url='http://data.bnf.fr/ark:/12148/cb118905823#foaf:Person')
    thing.add_query_endpoints([Endpoint.bnf])
    thing.query(strict_mode=True)
    assert u'http://viaf.org/viaf/17218730' in thing.attributes.get(u'owl:sameAs')


####################################################
#                 OTHER METHODS
####################################################

def test_thing_add_query_endpoints():
    """Thing - add_query_endpoints: Should pass"""
    thing = Thing()
    all_endpoints = set([e for e in Endpoint if not e == Endpoint.DEFAULT])
    thing.add_query_endpoints(all_endpoints)
    assert thing.endpoints == all_endpoints


def test_thing_deepen_search():
    """Thing - deepen_search(): Should pass"""
    endpoints = [Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf]
    thing = Thing(url='http://data.bnf.fr/ark:/12148/cb118905823#foaf:Person')
    thing.add_query_endpoints(endpoints)
    thing.query(strict_mode=True)
    attr_before_deep_search = len(thing.attributes)
    thing.deepen_search()
    attr_after_deep_search = len(thing.attributes)
    assert attr_before_deep_search < attr_after_deep_search


@raises(QueryException)
def test_thing_bad_language():
    """Thing - wrong language definition: Should fail"""
    thing = Thing(query_language="fr")

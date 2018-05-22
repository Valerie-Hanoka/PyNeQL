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

# Test queries content

def test_query_content_base_case():
    pass


def test_query_content_multiple_labels_checktype_strictmode():
    """Thing - query multiple labels - check_type=True, strict_mode=True: Should pass"""
    thing = Thing(
        label=["A", 2, "http://exemple.org/B"],
        limit=1,
        endpoints=[e for e in Endpoint]
    )

    thing.query(check_type=True, strict_mode=True)
    expected_queries = {
        Endpoint.DEFAULT: u'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt_o: <http://www.wikidata.org/ontology#> PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX schema: <http://schema.org/> SELECT DISTINCT ?Thing ?pred ?obj WHERE { ?Thing ?pred ?obj . { ?Thing a wdt_o:Item  } UNION { ?Thing a owl:Class  } UNION { ?Thing a schema:Thing  } UNION { ?Thing a wd:Q35120  } UNION { ?Thing a owl:Thing  } UNION { ?Thing a schema:Class  } UNION { ?Thing a dbo:Thing  } .  { ?Thing ?has_label "A"@en  } UNION { ?Thing ?has_label 2  } UNION { ?Thing ?has_label <http://exemple.org/B>  } .  } LIMIT 1',
        Endpoint.wikidata: u'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt_o: <http://www.wikidata.org/ontology#> PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX schema: <http://schema.org/> SELECT DISTINCT ?Thing ?pred ?obj WHERE { SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } ?Thing ?pred ?obj . { ?Thing a wdt_o:Item  } UNION { ?Thing a owl:Class  } UNION { ?Thing a schema:Thing  } UNION { ?Thing a wd:Q35120  } UNION { ?Thing a owl:Thing  } UNION { ?Thing a schema:Class  } UNION { ?Thing a dbo:Thing  } .  { ?Thing ?has_label "A"@en  } UNION { ?Thing ?has_label 2  } UNION { ?Thing ?has_label <http://exemple.org/B>  } .  } LIMIT 1',
        Endpoint.dbpedia_fr: u'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt_o: <http://www.wikidata.org/ontology#> PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX schema: <http://schema.org/> SELECT DISTINCT ?Thing ?pred ?obj WHERE { ?Thing ?pred ?obj . { ?Thing a wdt_o:Item  } UNION { ?Thing a owl:Class  } UNION { ?Thing a schema:Thing  } UNION { ?Thing a wd:Q35120  } UNION { ?Thing a owl:Thing  } UNION { ?Thing a schema:Class  } UNION { ?Thing a dbo:Thing  } .  { ?Thing ?has_label "A"@en  } UNION { ?Thing ?has_label 2  } UNION { ?Thing ?has_label <http://exemple.org/B>  } .  } LIMIT 1',
        Endpoint.bnf: u'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt_o: <http://www.wikidata.org/ontology#> PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX schema: <http://schema.org/> SELECT DISTINCT ?Thing ?pred ?obj WHERE { ?Thing ?pred ?obj . { ?Thing a wdt_o:Item  } UNION { ?Thing a owl:Class  } UNION { ?Thing a schema:Thing  } UNION { ?Thing a wd:Q35120  } UNION { ?Thing a owl:Thing  } UNION { ?Thing a schema:Class  } UNION { ?Thing a dbo:Thing  } .  { ?Thing ?has_label "A"  } UNION { ?Thing ?has_label 2  } UNION { ?Thing ?has_label <http://exemple.org/B>  } .  } LIMIT 1'
    }

    for e in Endpoint:
        assert fuzz.token_sort_ratio(expected_queries[e], thing.query_builder.queries[e]) > 90


def test_query_content_multiple_labels_checktype_nostrictmode():
    """Thing - query multiple labels - check_type=True, strict_mode=False: Should pass"""
    thing = Thing(
        label=["A", 2, "http://exemple.org/B"],
        limit=1,
        endpoints=[e for e in Endpoint]
    )

    thing.query(check_type=True, strict_mode=True)
    expected_queries = {
        Endpoint.DEFAULT: u'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt_o: <http://www.wikidata.org/ontology#> PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX schema: <http://schema.org/> SELECT DISTINCT ?Thing ?pred ?obj WHERE { ?Thing ?pred ?obj . { ?Thing a wdt_o:Item  } UNION { ?Thing a owl:Class  } UNION { ?Thing a schema:Thing  } UNION { ?Thing a wd:Q35120  } UNION { ?Thing a owl:Thing  } UNION { ?Thing a schema:Class  } UNION { ?Thing a dbo:Thing  } .  { ?Thing ?has_label "A"@en  } UNION { ?Thing ?has_label 2  } UNION { ?Thing ?has_label <http://exemple.org/B>  } .  } LIMIT 1',
        Endpoint.wikidata: u'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt_o: <http://www.wikidata.org/ontology#> PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX schema: <http://schema.org/> SELECT DISTINCT ?Thing ?pred ?obj WHERE { SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } ?Thing ?pred ?obj . { ?Thing a wdt_o:Item  } UNION { ?Thing a owl:Class  } UNION { ?Thing a schema:Thing  } UNION { ?Thing a wd:Q35120  } UNION { ?Thing a owl:Thing  } UNION { ?Thing a schema:Class  } UNION { ?Thing a dbo:Thing  } .  { ?Thing ?has_label "A"@en  } UNION { ?Thing ?has_label 2  } UNION { ?Thing ?has_label <http://exemple.org/B>  } .  } LIMIT 1',
        Endpoint.dbpedia_fr: u'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt_o: <http://www.wikidata.org/ontology#> PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX schema: <http://schema.org/> SELECT DISTINCT ?Thing ?pred ?obj WHERE { ?Thing ?pred ?obj . { ?Thing a wdt_o:Item  } UNION { ?Thing a owl:Class  } UNION { ?Thing a schema:Thing  } UNION { ?Thing a wd:Q35120  } UNION { ?Thing a owl:Thing  } UNION { ?Thing a schema:Class  } UNION { ?Thing a dbo:Thing  } .  { ?Thing ?has_label "A"@en  } UNION { ?Thing ?has_label 2  } UNION { ?Thing ?has_label <http://exemple.org/B>  } .  } LIMIT 1',
        Endpoint.bnf: u'PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wdt_o: <http://www.wikidata.org/ontology#> PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX schema: <http://schema.org/> SELECT DISTINCT ?Thing ?pred ?obj WHERE { ?Thing ?pred ?obj . { ?Thing a wdt_o:Item  } UNION { ?Thing a owl:Class  } UNION { ?Thing a schema:Thing  } UNION { ?Thing a wd:Q35120  } UNION { ?Thing a owl:Thing  } UNION { ?Thing a schema:Class  } UNION { ?Thing a dbo:Thing  } .  { ?Thing ?has_label "A"  } UNION { ?Thing ?has_label 2  } UNION { ?Thing ?has_label <http://exemple.org/B>  } .  } LIMIT 1'
    }

    for e in Endpoint:
        assert fuzz.token_sort_ratio(expected_queries[e], thing.query_builder.queries[e]) > 90




def test_query_content_multiple_labels_nochecktype_strictmode():
    """Thing - query multiple labels - check_type=False, strict_mode=True: Should pass"""
    thing = Thing(
        label=["A", 2, "http://exemple.org/B"],
        limit=1,
        endpoints=[e for e in Endpoint]
    )

    thing.query(check_type=False, strict_mode=True)
    expected_queries = {
        Endpoint.DEFAULT: u' SELECT DISTINCT ?Thing ?pred ?obj WHERE { ?Thing ?pred ?obj . { ?Thing ?has_label <http://exemple.org/B>  } UNION { ?Thing ?has_label "A"@en  } UNION { ?Thing ?has_label 2  } .  } LIMIT 1',
        Endpoint.wikidata: u' SELECT DISTINCT ?Thing ?pred ?obj WHERE { SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } ?Thing ?pred ?obj . { ?Thing ?has_label <http://exemple.org/B>  } UNION { ?Thing ?has_label "A"@en  } UNION { ?Thing ?has_label 2  } .  } LIMIT 1',
        Endpoint.dbpedia_fr: u' SELECT DISTINCT ?Thing ?pred ?obj WHERE { ?Thing ?pred ?obj . { ?Thing ?has_label <http://exemple.org/B>  } UNION { ?Thing ?has_label "A"@en  } UNION { ?Thing ?has_label 2  } .  } LIMIT 1',
        Endpoint.bnf: u' SELECT DISTINCT ?Thing ?pred ?obj WHERE { ?Thing ?pred ?obj . { ?Thing ?has_label <http://exemple.org/B>  } UNION { ?Thing ?has_label "A"  } UNION { ?Thing ?has_label 2  } .  } LIMIT 1'
    }

    for e in Endpoint:
        assert fuzz.token_sort_ratio(expected_queries[e], thing.query_builder.queries[e]) > 90





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
   assert thing.attributes

def test_thing_dbpedia_query_strict_False():
   """Thing - dbpedia - strict=False - : Should pass """
   thing = Thing(label=u"Paris", query_language=Lang.French, limit=666)
   thing.add_query_endpoint(Endpoint.dbpedia)
   thing.query(strict_mode=False)

   expected = {
       'endpoints': set([Endpoint.dbpedia]),
       'has_label': u"Paris",
       'query_language': Lang.French,
   }
   assert thing.endpoints == expected.get('endpoints')
   assert thing.has_label == expected.get('has_label')
   assert thing.query_language == expected.get('query_language')
   assert thing.attributes
   assert thing.labels_by_languages


# Testing Endpoint: dbpedia_fr

def test_thing_dbpedia_fr_query_strict_True():
   """Thing - dbpedia_fr - strict=True - : Should pass """
   label = "Acide pinique"
   thing = Thing(label=label, query_language=Lang.French)
   thing.add_query_endpoint(Endpoint.dbpedia_fr)
   thing.query(strict_mode=True)

   assert thing.endpoints == set([Endpoint.dbpedia_fr])
   assert thing.has_label == u'Acide pinique'
   assert thing.query_language == Lang.French
   assert thing.attributes
   assert thing.labels_by_languages


def test_thing_dbpedia_fr_query_strict_False():
   """Thing - dbpedia_fr - strict=False - : Should pass """

   label = u"11e régiment du génie"
   thing = Thing(label=label, query_language=Lang.French)
   thing.add_query_endpoint(Endpoint.dbpedia_fr)
   thing.query(strict_mode=False)

   assert thing.endpoints == set([Endpoint.dbpedia_fr])
   assert thing.has_label == u'11e r\xe9giment du g\xe9nie'
   assert thing.query_language == Lang.French
   assert thing.labels_by_languages
   assert thing.attributes


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
   PREFIX schema: <http://schema.org/>
   PREFIX dbo: <http://dbpedia.org/ontology/>
   PREFIX wdt_o: <http://www.wikidata.org/ontology#>
   SELECT DISTINCT ?Thing ?pred ?obj WHERE {
   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
   ?Thing ?pred ?obj .
   { ?Thing a owl:Class  } UNION
   { ?Thing a schema:Class  } UNION
   { ?Thing a wd:Q35120  } UNION
   { ?Thing a schema:Thing  } UNION
   { ?Thing a wdt_o:Item  } UNION
   { ?Thing a dbo:Thing  } UNION
   { ?Thing a owl:Thing  } .
   } LIMIT 1500
   """
   ratio = fuzz.token_sort_ratio(thing.query_builder.queries[Endpoint.wikidata], expected_query)
   assert ratio > 90


def test_thing_wikidata_query_strict_False():
   """Thing - wikidata - strict=True, check_type=False - : Should pass"""
   thing = Thing(label=u"혁kστ혁ηjh혁kي혁ةsjdジアh", query_language=Lang.DEFAULT)
   thing.add_query_endpoint(Endpoint.wikidata)
   thing.query(strict_mode=True, check_type=False)

   assert thing.endpoints == set([Endpoint.wikidata])
   assert thing.has_label == u'혁kστ혁ηjh혁kي혁ةsjdジアh'
   assert thing.query_language == Lang.English

   expected_query = u'''
   PREFIX wdt: <http://www.wikidata.org/prop/direct/>
   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
   SELECT DISTINCT ?Thing ?pred ?obj WHERE
   { SERVICE wikibase:label
    { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
     ?Thing ?pred ?obj .
     { ?Thing rdfs:label "혁kστ혁ηjh혁kي혁ةsjdジアh"@en  }
     UNION { ?Thing wdt:P1813 "혁kστ혁ηjh혁kي혁ةsjdジアh"@en  } .
       } LIMIT 1500'''

   ratio = fuzz.token_sort_ratio(thing.query_builder.queries[Endpoint.wikidata], expected_query)
   assert ratio > 90


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
   thing = Thing(
       url='http://dbpedia.org/resource/Charles_Baudelaire',
       endpoints=[e for e in Endpoint]
   )
   thing.query(strict_mode=True)
   assert u'http://dbpedia.org/resource/Charles_Baudelaire' in thing.attributes.get(u'owl:sameAs')


def test_thing_query_URLs():
   """Thing - URLs list query - : Should pass """

   thing = Thing(url=[
       'http://viaf.org/viaf/17218730',
       'http://www.wikidata.org/entity/Q501',
       'http://dbpedia.org/resource/Charles_Baudelaire'
   ])

   thing.add_query_endpoints([e for e in Endpoint])
   thing.query(strict_mode=True)
   assert u'http://dbpedia.org/resource/Charles_Baudelaire' in thing.attributes.get(u'owl:sameAs')



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
   """Thing - find_more_about(): Should pass"""
   endpoints = [Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf]
   thing = Thing(url='http://dbpedia.org/resource/Charles_Baudelaire')
   thing.add_query_endpoints(endpoints)
   thing.query(strict_mode=True)
   attr_before_deep_search = len(thing.attributes)
   thing.find_more_about()
   attr_after_deep_search = len(thing.attributes)
   assert attr_before_deep_search < attr_after_deep_search


@raises(QueryException)
def test_thing_bad_language():
   """Thing - wrong language definition: Should fail"""
   thing = Thing(query_language="fr")

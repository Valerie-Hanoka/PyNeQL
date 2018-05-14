#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_genericsparqlquery is part of the project PyNeQL
Author: Valérie Hanoka

"""

from nose.tools import *

from fuzzywuzzy import fuzz

from pyneql.query.querybuilder import GenericSPARQLQuery
from pyneql.query.rdftriple import RDFTriple
from pyneql.utils.namespace import NameSpace
from pyneql.utils.endpoints import Endpoint
from pyneql.utils.utils import QueryException



#---------------------------------------
#          RDF Triples
#---------------------------------------

def test_genericsparqlquery_base_case():
    """GenericSPARQLQuery - Base case, no issues: Should pass"""

    query = GenericSPARQLQuery()

    simone = RDFTriple(
        subject=u'?person',
        object=u'"Simone de Beauvoir"@fr',
        predicate=u'rdfs:label')

    birth = RDFTriple(
        subject =u'?person',
        object=u'?birthdate',  #1908-01-09
        predicate=u'dbpedia_owl:birthDate',
        prefixes=[NameSpace.dbpedia_owl],
    )
    gender = RDFTriple(
        subject=u'?person',
        object=u'?gender',
        predicate=u'<http://xmlns.com/foaf/0.1/gender>',
    )

    triples = [simone, birth, gender]
    query.add_query_triples(triples)
    query.set_limit(10)
    query.commit()

    true_prefixes = {NameSpace.foaf, NameSpace.dbpedia_owl, NameSpace.rdfs}
    assert not set(query.prefixes).difference(true_prefixes)
    assert not query.endpoints.difference({Endpoint.DEFAULT})
    assert not set(query.triples).difference(set(triples))
    assert query.limit == u'LIMIT 10'

    truth_query = u'PREFIX foaf: <http://xmlns.com/foaf/0.1/> ' \
                  u'PREFIX dbo: <http://dbpedia.org/ontology/> ' \
                  u'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> ' \
                  u'SELECT DISTINCT * WHERE {' \
                  u' ?person rdfs:label "Simone de Beauvoir"@fr .' \
                  u' ?person dbo:birthDate ?birthdate .' \
                  u' ?person foaf:gender ?gender . ' \
                  u'} ' \
                  u'LIMIT 10'

    ratio = fuzz.token_sort_ratio(query.queries[Endpoint.DEFAULT], truth_query)
    assert ratio==100

    truth_results = [
        [
            ('person', 'http://dbpedia.org/resource/Simone_de_Beauvoir'),
            ('birthdate', '1908-01-09'),
            ('gender', 'female _(@en)')],
        [
            ('person', 'http://dbpedia.org/resource/Simone_de_Beauvoir'),
            ('birthdate', '1908-1-9'),
            ('gender', 'female _(@en)')
        ]
    ]

    assert query.results == truth_results

def test_genericsparqlquery_add_prefixes():
    """GenericSPARQLQuery.add_prefix() - Base case, no issues: Should pass"""
    query = GenericSPARQLQuery()
    query.add_prefixes(['foaf: <http://xmlns.com/foaf/0.1/>', 'bar: <http://baz.com/foo/0.1/>'])
    assert query.prefixes == set([NameSpace.foaf, NameSpace.bar])


def test_genericsparqlquery_add_endpoints():
    """GenericSPARQLQuery.add_endpoint.s() - Base case, no issues: Should pass"""

    query = GenericSPARQLQuery()
    query.add_endpoint(Endpoint.dbpedia)
    assert query.endpoints == set([Endpoint.dbpedia])

    query.add_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr])
    assert query.endpoints == set([Endpoint.dbpedia, Endpoint.bnf, Endpoint.dbpedia_fr])

@raises(QueryException)
def test_genericsparqlquery_add_endpoints_unsupported_endpoint():
    """GenericSPARQLQuery.add_endpoints() - Unsupported endpoint: Should fail"""
    query = GenericSPARQLQuery()
    query.add_endpoints([Endpoint.bnf, "www.foo.bar.com/sparql"])


@raises(QueryException)
def test_genericsparqlquery_set_limit_unsupported_limit1():
    """GenericSPARQLQuery.set_limit() - Unsupported limit: Should fail"""
    query = GenericSPARQLQuery()
    query.set_limit("42")


@raises(QueryException)
def test_genericsparqlquery_set_limit_unsupported_limit2():
    """GenericSPARQLQuery.set_limit() - Unsupported limit: Should fail"""
    query = GenericSPARQLQuery()
    query.set_limit(0)


@raises(QueryException)
def test_genericsparqlquery__validate_arguments_bad_query1():
    """GenericSPARQLQuery._validate_arguments() - Empty query: Should fail"""
    query = GenericSPARQLQuery()
    query.commit()

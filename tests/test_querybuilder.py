#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_genericsparqlquery is part of the project PyNeQL
Author: Valérie Hanoka

"""

from fuzzywuzzy import fuzz
from pyneql.querybuilder import GenericSPARQLQuery
from pyneql.rdftriple import RDFTriple
from pyneql.namespace import NameSpace
from pyneql.enum import Endpoint


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
                  u'PREFIX dbpedia_owl: <http://dbpedia.org/ontology/> ' \
                  u'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> ' \
                  u'SELECT * WHERE { ' \
                  u'?person rdfs:label "Simone de Beauvoir"@fr . ' \
                  u'?person dbpedia_owl:birthDate ?birthdate . ' \
                  u'?person foaf:gender ?gender . ' \
                  u'} LIMIT 3'

    ratio = fuzz.ratio(query.query, truth_query)
    assert ratio > 98

    truth_results = {
        u'birthdate': {
            u'datatype': [u'http://www.w3.org/2001/XMLSchema#date',
                          u'http://www.w3.org/2001/XMLSchema#date'],
            u'type': [u'typed-literal', u'typed-literal'],
            u'value': [u'1908-01-09', u'1908-1-9']},
        u'gender': {
            u'type': [u'literal', u'literal'],
            u'value': [u'female', u'female'],
            u'xml:lang': [u'en', u'en']},
        u'person': {u'type': [u'uri', u'uri'],
                    u'value': [u'http://dbpedia.org/resource/Simone_de_Beauvoir',
                               u'http://dbpedia.org/resource/Simone_de_Beauvoir']}
    }

    assert cmp(query.results, truth_results) == 0

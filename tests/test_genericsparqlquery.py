#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_genericsparqlquery is part of the project PyNeQL
Author: Valérie Hanoka

"""

from nose.tools import *

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
    query.set_limit(3)
    query.commit()

    true_prefixes = set([
        NameSpace.foaf,
        NameSpace.dbpedia_owl,
        NameSpace.rdfs])

    assert set(query.prefixes).difference(true_prefixes) == 0
    # assert query.result_arguments == # TODO
    assert query.endpoints.difference(set([Endpoint.DEFAULT]))==0
    assert set(query.triples).difference(triples) == 0
    # TODO assert query.query_results ==
    assert query.limit == u'LIMIT 3'
    assert query.query == u'PREFIX foaf: <http://xmlns.com/foaf/0.1/> PREFIX dbpedia_owl:' \
                          u' <http://dbpedia.org/ontology/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> ' \
                          u'SELECT * WHERE { ' \
                          u'?person rdfs:label "Simone de Beauvoir"@fr .' \
                          u' ?person dbpedia_owl:birthDate ?birthdate .' \
                          u' ?person foaf:gender ?gender .' \
                          u' } LIMIT 3'

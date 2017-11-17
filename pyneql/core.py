#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from enum import Endpoint as ep
from querybuilder import GenericSPARQLQuery
from rdftriple import RDFTriple
from namespace import NameSpace

from fuzzywuzzy import fuzz



query = GenericSPARQLQuery()

simone = RDFTriple(
    subject=u'?person',
    object=u'"Simone de Beauvoir"@fr',
    predicate=u'rdfs:label')

birth = RDFTriple(
    subject=u'?person',
    object=u'?birthdate',  # 1908-01-09
    predicate=u'dbpedia_owl:birthDate',
    prefixes=[NameSpace.dbpedia_owl],
)
gender = RDFTriple(
    subject=u'?person',
    object=u'?gender',
    predicate=u'<http://xmlns.com/foaf/0.1/gender>',
)

query.add_query_triples([simone, birth, gender])
query.set_limit(3)
query.commit()

truth_query = u'PREFIX foaf: <http://xmlns.com/foaf/0.1/> ' \
              u'PREFIX dbpedia_owl: <http://dbpedia.org/ontology/> ' \
              u'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> ' \
              u'SELECT * WHERE { ' \
              u'?person rdfs:label "Simone de Beauvoir"@fr . ' \
              u'?person dbpedia_owl:birthDate ?birthdate . ' \
              u'?person foaf:gender ?gender . ' \
              u'} LIMIT 3'

ratio = fuzz.ratio(query.query, truth_query)

import ipdb; ipdb.set_trace()



#q.query(name, language)



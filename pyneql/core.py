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

import ipdb; ipdb.set_trace()



#q.query(name, language)



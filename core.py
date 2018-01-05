#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka
"""

# Debug:

#from pyneql.ontology.person import Person
#from pyneql.utils.enum import LanguagesIso6391 as Lang
#from pyneql.utils.endpoints import Endpoint

# db = dataset.connect(u'sqlite:////Users/hanoka/obvil/TEIExplorer/useAndReuse.db')
# person_table = db['person']
#
# endpoints = [Endpoint.wikidata, Endpoint.bnf, Endpoint.dbpedia_fr, Endpoint.dbpedia]
# endpoints_scores = {}
#
# for endpoint in endpoints:
#     people = {}
#     endpoints_scores[endpoint] = {}
#     for row in person_table:
#         (first_name, last_name) = row.get('first_name_or_initials').strip(), row.get('last_name').strip()
#         full_name = u'%s %s' % (first_name, last_name)
#         try:
#             birth = int(row.get('birth', "None") or "None")
#         except ValueError:
#             birth = None
#         try:
#             death = int(row.get('death', "None")or "None")
#         except ValueError:
#             death = None
#
#         fingerprint = u"%s %s %s" % (
#             full_name.strip(),
#             birth,
#             death
#         )
#         people[fingerprint] = {}
#
#         print("%s  ---  %s" % (row.get('fingerprint'), fingerprint, ))
#
#         if first_name and last_name:
#             person = Person(
#                 full_name=full_name.strip(),
#                 last_name=last_name,
#                 # birth_year=birth,
#                 # death_year=death,
#                 query_language=Lang.French
#             )
#             person.add_query_endpoint(endpoint)
#             person.query()
#
#             if person.attributes:
#                 people[fingerprint]['sw_birth'] = person.get_birth_info()
#                 people[fingerprint]['sw_death'] = person.get_death_info()
#                 people[fingerprint]['external_ids'] = person.get_external_ids()
#                 people[fingerprint]['mouvement'] = person.attributes.get(u'prop_fr:mouvement')
#
#             else:
#                 people[fingerprint]['NOT FOUND'] = True
#             people[fingerprint]['old_fingerprint'] = row.get('fingerprint')
#
#             not_found = [p for (p, a) in people.iteritems() if a.get('NOT FOUND', False)]
#
#     endpoints_scores[endpoint]['Total'] = len(people)
#     endpoints_scores[endpoint]['Not found'] = len(not_found)
#     endpoints_scores[endpoint]['rate'] = len(not_found)*100.0/len(people)
#     print("Total: %i | Not found: %i " %(len(people), len(not_found)))


# duras = Person(full_name="Marguerite Duras", query_language=Lang.French)
# duras.add_query_endpoint(Endpoint.wikidata)
# duras.query()

from fuzzywuzzy import fuzz

from pyneql.ontology.person import Person
from pyneql.utils.endpoints import Endpoint
from pyneql.utils.enum import LanguagesIso6391 as Lang

duras = Person(first_name="Marguerite", last_name="Duras", query_language=Lang.French)
duras.add_query_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr])
duras.query()

import ipdb; ipdb.set_trace()






#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka
"""

# Debug:

from pyneql.ontology.person import Person
from pyneql.utils.enum import LanguagesIso6391 as Lang
from pyneql.utils.endpoints import Endpoint
import dataset

import pprint

endpoints = [Endpoint.dbpedia, Endpoint.wikidata , Endpoint.bnf, Endpoint.dbpedia_fr]

db = dataset.connect(u'sqlite:////Users/hanoka/obvil/TEIExplorer/useAndReuse.db')


book_table = db['identifier']





import ipdb; ipdb.set_trace()

# person_table = db['person']
# people = {}
# for row in person_table:
#     (first_name, last_name) = row.get('first_name_or_initials').strip(), row.get('last_name').strip()
#     full_name = u'%s %s' % (first_name, last_name)
#     try:
#         birth = int(row.get('birth', "None") or "None")
#     except ValueError:
#         birth = None
#     try:
#         death = int(row.get('death', "None")or "None")
#     except ValueError:
#         death = None
#
#     fingerprint = u"%s %s %s" % (
#         full_name.strip(),
#         birth,
#         death
#     )
#     print("%s  ---  %s" % (row.get('fingerprint'), fingerprint, ))
#     if first_name and last_name:
#         person = Person(
#             full_name=full_name.strip(),
#             query_language=Lang.French
#         )
#         person.add_query_endpoints(endpoints)
#         person.query()
#
#         if person.attributes:
#             people[fingerprint] = person
#
#         else:
#             people[fingerprint] = None
#         people[fingerprint]['old_fingerprint'] = row.get('fingerprint')










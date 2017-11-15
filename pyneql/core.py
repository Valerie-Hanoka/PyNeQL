#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka

"""
import logging
from enum import LanguagesIso6391 as Lang
from querybuilder import GenericSPARQLQuery as Query

name = u"Simone de Beauvoir"
language = Lang.French

q = Query()

t = {u'predicate': u'rdfs:label', u'object': u'"Simone de Beauvoir"@fr'}
q.add_query_triple(**t)
q.commit()

# query.set_endpoints( endpoints_list )
# query.add_filters( filters_list )
# query.limit( limit_int )
# query.result_language( lang_list)
# query.result_types( type_list )

#q.query(name, language)


import ipdb; ipdb.set_trace()

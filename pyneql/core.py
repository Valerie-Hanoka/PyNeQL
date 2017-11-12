#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka

"""
import logging
from enum import LanguagesIso6391 as Lang
from querybuilder import GenericSPARQLQuery as Query

name = "Simone de Beauvoir"
language = Lang.French

query = Query()
query.what(name, language)


# query.set_endpoints( endpoints_list )
# query.add_filters( filters_list )
# query.limit( limit_int )
# query.result_language( lang_list)
# query.result_types( type_list )

import ipdb; ipdb.set_trace()

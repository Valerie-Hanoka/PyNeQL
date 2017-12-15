#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from person import Person
from enum import (
    Endpoint,
    LanguagesIso6391 as Lang
)

duras = Person(first_name="Marguerite", last_name="Duras", query_language=Lang.French)
duras.add_query_endpoints([Endpoint.dbpedia_fr, Endpoint.bnf, Endpoint.dbpedia])  # Endpoint.dbpedia, Endpoint.dbpedia_fr
duras.query()

pprint(duras.attributes)









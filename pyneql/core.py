#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from personquerybuilder import PersonQuery
from enum import Endpoint
from pprint import pprint

duras = PersonQuery(first_name="Marguerite", last_name="Duras")
duras.add_endpoints([Endpoint.bnf, Endpoint.dbpedia_fr])  # Endpoint.dbpedia, Endpoint.dbpedia_fr
duras.query()

pprint(duras.attributes)


import ipdb; ipdb.set_trace()




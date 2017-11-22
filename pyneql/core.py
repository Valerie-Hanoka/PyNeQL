#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from personquerybuilder import PersonQuery
from enum import Endpoint

person = PersonQuery(first_name="Marguerite", last_name="Duras")

# TODO: BnF 403 http code
person.add_endpoints([Endpoint.bnf])  # , Endpoint.dbpedia, Endpoint.dbpedia_fr
person.query()

import ipdb; ipdb.set_trace()




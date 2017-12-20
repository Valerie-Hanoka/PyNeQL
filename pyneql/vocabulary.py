#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vocabulary.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from aenum import Enum

rdf_types = {
    u'Person': {
        "foaf:Person",
        "dbpedia_owl:Person",
        "schemaorg:Person"
        }
}

# Curated list of predicates giving access to an Named Entity's attribute in the endpoints:
#        - DBPedia
# TODO: more endpoints

attributes = {
    u'Person': {
        u'has_first_name': [
            u'dbpprop:firstname',
            u'foaf:givenName',
            u'dbpprop:givenname'
        ],
        u'has_last_name': [
            u'foaf:surname',
            u'foaf:familyName',
            u'dbpprop:lastname',
            u'dbpprop:maidenname',
            u'dbpprop:surname'
        ],
        u'has_full_name': [
            u'dbpprop:birthname',
            u'dbpprop:birthnames',
            u'dbpprop:fullname',
            u'dbpprop:name',
            u'foaf:name'
        ],
        u'has_alternative_names': [
            u'dbpprop:altname',
            u'dbpprop:nickname',
            u'dbpprop:nicknames',
            u'dbpedia_owl:alias',
            u'dbpprop:alias',
            u'dbpprop:aliases',
            u'dbpprop:nomAlias',
            u'dbpprop:othername',
            u'dbpprop:othernames'
        ]
    }
}


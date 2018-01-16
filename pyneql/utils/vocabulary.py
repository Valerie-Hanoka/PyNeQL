#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vocabulary.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

rdf_types = {
    u'Thing': {
        "dbo:Thing",
        "owl:Class",
        "owl:Thing",
        "wd:Q35120",  # Wikidata for entity.
        "schema:Thing",
        "schema:Class",
        "wdt_o:Item"
    },
    u'Person': {
        "foaf:Person",
        "dbpedia_owl:Person",
        "wd:Q5",  # Wikidata for a human being.
        "dul:NaturalPerson",
        "schema:Person"
    }
}

# Curated list of predicates giving access to an Named Entity's attribute in the endpoints.
# TODO: Some prefixes have same vocabulary and are not recognized. Should expand doubles.
# E.g: wikidata = wdt

# N.B. the attributes names must correspond to the 'has_...' of the corresponding class.
attributes = {
    u'Thing': {
        u'has_foo': [u'foo:bar', u'foo:baz'],  # For the example
        u'has_label': [u'rdfs:label']
    },
    u'Person': {
        u'has_first_name': [
            u'dbpprop:firstname',
            u'foaf:givenName',
            u'dbpprop:givenname',
            u'wikidata:P735', # given name
            u'schemaorg:givenName',
            u'vcard2006:given-name',
        ],
        u'has_last_name': [
            u'foaf:surname',
            u'foaf:familyName',
            u'dbpprop:lastname',
            u'dbpprop:maidenname',
            u'dbpprop:surname',
            u'wdt:P734', # family name
            u'wdt:P1950', # second family name in Spanish name
            u'schema:familyName',
            u'vcard2006:family-name',
        ],
        u'has_full_name': [
            u'dbpprop:birthname',
            u'dbpprop:birthnames',
            u'dbpprop:fullname',
            u'dbpprop:name',
            u'foaf:name',
            u'wdt:P1477',
            u'wdt:P2561',
            u'wdt:P1559',
            u'dbo:birthName',
            u'rdfs:label'
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
            u'dbpprop:othernames',
            u'foaf:nick'
        ],
        u'has_death_date': [
            u'wdt:P570',  # date of death
            u'wdt:P746',  # date of disappearance
            u'schema:deathDate',
            u'bnf_onto:lastYear',
            u'bio:death'
        ],
        u'has_birth_date': [
            u'wdt:P569',
            u'schema:birthDate',
            u'vcard2006:bday',
            u'bnf_onto:firstYear',
            u'bio:birth'
        ],
    }
}

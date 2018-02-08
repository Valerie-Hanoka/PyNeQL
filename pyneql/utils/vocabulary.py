#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vocabulary.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

# ----------------------------------- #
#      Ontology Objects Types
# ----------------------------------- #

rdf_types = {
    # THING
    u'Thing': {
        u"dbo:Thing",
        u"owl:Class",
        u"owl:Thing",
        u"wd:Q35120",                          # Wikidata for entity.
        u"schema:Thing",
        u"schema:Class",
        u"wdt_o:Item"
    },
    # PERSON
    u'Person': {
        u"foaf:Person",
        u"dbpedia_owl:Person",
        u"wd:Q5",                              # Wikidata for a human being.
        u"dul:NaturalPerson",
        u"schema:Person"
    },
    # BOOK
    u'Book': {
        u"wd:Q571",                            # Wikidata for Book
        u"wd:Q7725634",                        # Wikidata for a literary work.
        u"schema:Book",
        u'schemaorg:Book',
        u"schema:Thesis",
        u"dbpedia_owl:Book",
        u'dbo:Book',
        u"dbpedia_owl:WrittenWork",            # Superclass
        u"fabio:Book",
        u"bibo:Book",
        u'frbr_rda:Work',
        u'frbr_rda:Manifestation',
        u'dbo:WrittenWork',
        u'foaf:Document'
    }
}


# --------------------------------------- #
#   Ontology Objects Attributes Types
# --------------------------------------- #
# Curated list of predicates giving access to an Named Entity's attribute in the endpoints.
# N.B. the attributes names must correspond to the 'has_...' of the corresponding class.
# TODO: Some prefixes have same vocabulary and are not recognized. Should expand doubles. E.g: wikidata = wdt

attributes = {
    # THING
    u'Thing': {
        u'has_label': [u'rdfs:label', u'wdt:P1813']
    },

    # PERSON
    u'Person': {
        u'has_first_name': [
            u'dbpprop:firstname',
            u'foaf:givenName',
            u'dbpprop:givenname',
            u'wdt:P735',                                # given name
            u'schemaorg:givenName',
            u'vcard2006:given-name',
        ],
        u'has_last_name': [
            u'foaf:surname',
            u'foaf:familyName',
            u'dbpprop:lastname',
            u'dbpprop:maidenname',
            u'dbpprop:surname',
            u'wdt:P734',                               # family name
            u'wdt:P1950',                              # second family name in Spanish
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
            u'foaf:nick',
            u'skos:altLabel'
        ],
        u'has_death_date': [
            u'wdt:P570',                                # date of death
            u'wdt:P746',                                # date of disappearance
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
    },

    # BOOK
    u'Book': {
        u'has_author': [
            u'wdt:P50',                                 # author
            u'wdt:P1773',                               # attributed to
            u'wdt:P2093',                               # author name string
            u'schema:author',
            u'schema:creator',
            u'dcterms:creator',
            u'dbo:author',
            u'bnfroles:r70'
        ],
        u'has_title': [
            u'schema:alternativeHeadline',
            u'schema:alternateName',
            u'schema:name',
            u'dcterms:title'
        ],
        u'has_isbn': [
            u'schema:isbn',
        ],
        u'has_publicatin_date': [
            u'schema:datePublished',
            u'bnf_onto:firstYear',
            u'wdt:P577'
        ],
        u'has_publisher': [
            u'schema:publisher',
            u'dcterms:publisher',
            u'rdagroup1elements:publishersName'
        ],
        u'has_gallica_url': [
            u'http://rdvocab.info/RDARelationshipsWEMI/electronicReproduction'
        ]
    },
}

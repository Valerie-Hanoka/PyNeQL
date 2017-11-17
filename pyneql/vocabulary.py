#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vocabulary.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from aenum import Enum, extend_enum


rdf_types =  {
    u'person': {
        "foaf:Person",
        "dbpedia_owl:Person",
        "schemaorg:Person"
        }
}



class PersonName():
    """
    Curated list of predicates giving access to a person's name in the endpoints:
        - DBPedia
        TODO: More endpoints
    """

    class AlternativeName(Enum):
        altname = u'dbpprop:altname'
        nickname = u'dbpprop:nickname'
        nicknames = u'dbpprop:nicknames'
        owl_alias = u'dbpedia_owl:alias'
        dbpprop_alias = u'dbpprop:alias'
        dbpprop_aliases = u'dbpprop:aliases'
        nomalias = u'dbpprop:nomAlias'
        othername = u'dbpprop:othername'
        othernames = u'dbpprop:othernames'

    class FullName(Enum):
        birthname = u'dbpprop:birthname'
        birthnames = u'dbpprop:birthnames'
        fullname = u'dbpprop:fullname'
        dbpprop_name = u'dbpprop:name'
        foaf_name = u'foaf:name'

    class FirstName(Enum):  # Prénom
        firstname = u'dbpprop:firstname' # TODO: suppr ?
        givenname = u'dbpprop:givenname'

    class LastName(Enum):
        surname = u'foaf:surname'
        lastname = u'dbpprop:lastname' # TODO: suppr ?
        maidenname = u'dbpprop:maidenname'
        surname	= u'dbpprop:surname'



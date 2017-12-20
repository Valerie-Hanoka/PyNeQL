#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
personquerybuilder is part of the project PyNeQL
Author: Valérie Hanoka

"""

from thing import Thing
from loggingsetup import (
    setup_logging,
)

from querybuilder import GenericSPARQLQuery
from vocabulary import (
    rdf_types,
    attributes
)
from rdftriple import RDFTriple
from enum import (
    LanguagesIso6391 as Lang,
)

from namespace import get_shortened_uri
from utils import (
    QueryException,
    merge_two_dicts_in_sets
)


class Person(Thing):
    """
    A semantic representation of a person, retrieved from the Semantic Web.
    """

    setup_logging()

    # Elements which will be used to construct the query for a Person
    has_full_name = None
    has_last_name = None
    has_first_name = None

    def __init__(self,
                 full_name=None, last_name=None, first_name=None,
                 query_language=Lang.DEFAULT,
                 endpoints=None,  # SPARQL endpoints where the query should be sent
                 class_name=u'Person'
                 ):

        if not (full_name or (first_name and last_name)):
            raise QueryException("There is not enough information provided to find this person."
                                 " Provide full name information.")

        self.has_full_name = full_name
        self.has_last_name = last_name
        self.has_first_name = first_name
        super(Person, self).__init__(query_language=query_language, endpoints=endpoints, class_name=class_name)


    def _build_query(self):

        # Restricting the query to only Person elements
        # For the moment only foaf:Person, to keep it simple and efficient
        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=u'a',
                object=u'foaf:Person',
                language=self.query_language
            )
        )

        # Adding query delimiters
        entities_names = [e for e in self.__dict__.keys() if e.startswith('has_') and self.__dict__.get(e, False)]
        for entity_name in entities_names:
            tmp = self.__dict__.get(entity_name, None)
            obj = u'"%s"' % tmp if tmp else u'?%s' % entity_name
            pred = u'?%s' % entity_name
            self.query_builder.add_query_triple(
                RDFTriple(
                    subject=self.args['subject'],
                    predicate=pred,
                    object=obj,
                    language=self.query_language
                )
            )

        # Fetching everything about that person
        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=self.args['predicate'],
                object=self.args['object'],
                language=self.query_language
            )
        )


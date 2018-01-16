#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
book is part of the project PyNeQL
Author: Valérie Hanoka

"""

from pyneql.ontology.thing import Thing
from pyneql.log.loggingsetup import (
    setup_logging,
)

from pyneql.query.rdftriple import RDFTriple
from pyneql.utils.enum import (
    LanguagesIso6391 as Lang,
)

from pyneql.utils.endpoints import Endpoint
from pyneql.utils.utils import (
    QueryException,
    contains_a_date,
    merge_two_dicts_in_sets
)

class CreativeWork(Thing):
    """
    A semantic representation of a book, retrieved from the Semantic Web.
    """

    setup_logging()

    # Elements which will be used to construct the query for a Person
    has_title = None
    has_id = None
    has_author = None
    has_publication_date = None

    def __init__(self,
                 title=None,
                 author=None,
                 id=None,
                 publication_date=None,
                 query_language=Lang.DEFAULT,
                 endpoints=None,  # SPARQL endpoints where the query should be sent
                 class_name=u'CreativeWork'
                 ):

        if not (id or ((author or publication_date) and title)):
            raise QueryException("There is not enough information provided to find this creative work."
                                 " Provide more information.")

        self.has_title = title
        self.has_id = id
        self.has_author = author
        self.has_publication_date = publication_date
        super(CreativeWork, self).__init__(
            query_language=query_language,
            endpoints=endpoints,
            class_name=class_name
        )

    def _build_query(self):

        # Restricting the query to only CreativeWork elements
        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=u'wdt:P31',
                object=u'wd:Q5',
                keep_only_endpoints=[Endpoint.wikidata],
                language=self.query_language
            )
        )

        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=u'a',
                object=u'foaf:Person',
                excluded_endpoints=[Endpoint.wikidata],
                language=self.query_language
            )
        )

        # Adding query delimiters, that are the parameters given for query
        # (i.e stored in the instance variables begining with "has_").
        # For instance, Person(full_name="Jemaine Clement") will have its query
        # restrained to elements satisfying the triplet '?Person ?has_full_name "Jemaine Clement."'.
        entities_names = [e for e in self.__dict__.keys() if e.startswith('has_') and self.__dict__.get(e, False)]
        for entity_name in entities_names:
            tmp = self.__dict__.get(entity_name, None)
            if tmp:
                try:
                    # For dates elements, the triplet literal must be formatted without quotes
                    obj = int(tmp)
                except ValueError:
                    obj = u'"%s"' % tmp
            else:
                obj = u'?%s' % entity_name
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
personquerybuilder is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
from loggingsetup import (
    setup_logging,
    highlight_str
)

from querybuilder import GenericSPARQLQuery
from rdftriple import RDFTriple
from enum import (
    LanguagesIso6391 as Lang,
    Endpoint
)
from namespace import get_uri_last_part
from utils import (
    QueryException,
    merge_two_dicts_in_sets
)


class PersonQuery(object):
    """
    TODO
    """

    setup_logging()

    args = {
        'subject': u'?person',
        'predicate': u'?pred',
        'object': u'?obj'
    }

    # Elements which will be used to construct the query
    has_full_name = None
    has_last_name = None
    has_first_name = None

    # Query
    query_builder = None
    endpoints = None

    # Results
    results = None

    def __init__(self,
                 full_name=None, last_name=None, first_name=None,
                 query_language=Lang.DEFAULT,
                 endpoints=None  # SPARQL endpoints where the query should be sent
                 ):

        if not (full_name or (first_name and last_name)):
            raise QueryException("There is not enough information provided to find this person."
                                 " Provide full name information.")

        self.has_full_name = full_name
        self.has_last_name = last_name
        self.has_first_name = first_name

        self.query_language = query_language
        self.query_builder = GenericSPARQLQuery()

        self.endpoints = endpoints if endpoints else set([])
        self.results = {}

    def add_endpoints(self, endpoints):
        map(self.add_endpoint, endpoints)

    def add_endpoint(self, endpoint):
        self.endpoints.add(endpoint)

    def _build_query(self):

        # Restricting the query to only foaf:Person elements
        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=u'a',
                object=u'foaf:Person'
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
                    object=obj
                )
            )

        # Fetching everything about that person
        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=self.args['predicate'],
                object=self.args['object'])
        )

    def query(self):

        self._build_query()
        self.query_builder.add_endpoints(self.endpoints)
        wanna_know = [self.args['predicate'], self.args['object']]
        self.query_builder.add_result_arguments(wanna_know)
        self.query_builder.commit()
        self._get_results()

    def _get_results(self):
        """Given the result of a SPARQL query to find a Person,
        this creates a Person with all the information gathered."""

        to_dict = lambda (predicate, object): {predicate[1]: object[1]}
        for result in self.query_builder.results:
            self.results = merge_two_dicts_in_sets(
                self.results,
                to_dict(result)
            )


class PeriodQuery(object):
    """
    TODO: Time and period
    SELECT * WHERE
    { ?x
    rdfs:label
    "Renaissance" @ fr; ?y ?z.}
    pass
    """


class LocationQuery(object):
    """
    TODO: a place
    """

    options = {
        'query_term': "Max Power",
        'query_term_lang': Lang.DEFAULT,
    }


class MasterPieceQuery(object):
    """
    TODO: une oeuvre
    """

    options = {
        'query_term': "Max Power",
        'query_term_lang': Lang.DEFAULT,
    }
    # Dublin core



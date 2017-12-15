#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
personquerybuilder is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
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


class Person(object):
    """
    A semantic representation of a person, retrieved from the Semantic Web.
    """

    setup_logging()

    rdf_types = rdf_types[u'person']
    person_attributes = attributes[u'person']

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
    attributes = None

    def __init__(self,
                 full_name=None, last_name=None, first_name=None,
                 query_language=Lang.DEFAULT,
                 endpoints=None  # SPARQL endpoints where the query should be sent
                 ):

        if not (full_name or (first_name and last_name)):
            raise QueryException("There is not enough information provided to find this person."
                                 " Provide full name information.")
        if not isinstance(query_language, Lang):
            raise QueryException("The language of the query must be of type enum.LanguagesIso6391.")

        self.has_full_name = full_name
        self.has_last_name = last_name
        self.has_first_name = first_name

        self.query_builder = GenericSPARQLQuery()
        self.query_language = query_language

        self.endpoints = endpoints if endpoints else set([])
        self.attributes = {}

    def add_query_endpoints(self, endpoints):
        map(self.add_query_endpoint, endpoints)

    def add_query_endpoint(self, endpoint):
        self.endpoints.add(endpoint)

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

    def query(self):

        self._build_query()
        self.query_builder.add_endpoints(self.endpoints)
        wanna_know = [self.args['subject'], self.args['predicate'], self.args['object']]
        self.query_builder.add_result_arguments(wanna_know)
        self.query_builder.commit()
        self._process_results()

    def _process_results(self):
        """Given the result of a SPARQL query to find a Person,
        this creates a Person with all the information gathered."""

        values_to_check = {v: e for e, v in self.__dict__.items() if e.startswith('has_') and self.__dict__.get(e, False)}
        people = {}

        for result in self.query_builder.results:
            dict_results = {arg_name: get_shortened_uri(arg_value) for (arg_name, arg_value) in result}
            person = dict_results.pop(self.args['subject'][1:], None)

            # Checking that it is the person we are looking for
            if dict_results[self.args['object'][1:]] in values_to_check:
                value = dict_results[self.args['object'][1:]]
                properties = self.person_attributes.get(values_to_check[value], False)
                if properties and dict_results[self.args['predicate'][1:]] in properties:
                    people[person]["validated"] = 1

            shortened_result = {dict_results[u'pred']: dict_results[u'obj']}
            people[person] = merge_two_dicts_in_sets(people.get(person, {}), shortened_result)

        # Removing wrong people and adding the attributes of the correct person
        for person, person_attribute in people.items():
            if not person_attribute.get('validated', False):
                people.pop(person)
            else:
                self.attributes = merge_two_dicts_in_sets(self.attributes, {u'owl:sameAs': person})
                self.attributes = merge_two_dicts_in_sets(self.attributes, person_attribute)


    # def _get_names(self):
    #     from vocabulary import PersonName
    #
    #     for attribute in PersonName:
    #
    #
    #     PersonName.FullName


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



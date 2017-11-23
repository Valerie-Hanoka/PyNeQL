#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
querybuilder.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
from loggingsetup import (
    setup_logging,
    highlight_str
)

from utils import (
    QueryException,
)

from enum import (
    Endpoint,
    is_endpoint_multilingual
)

from namespace import (
    NameSpace,
    decompose_prefix,
    get_consistent_namespace,
    add_namespace
)

import requests
import json

#  ---------------------------------
#        SPARQL queries
#  ---------------------------------


class GenericSPARQLQuery(object):
    """A generic SPARQL 'select' query builder.
     It is used to build queries iteratively."""

    setup_logging()
    template_query = u'%(prefix)s SELECT %(result_arguments)s WHERE { %(triples)s } %(limit)s'

    def __init__(self):
        self.prefixes = set([])  # a set of vocabulary.prefixes
        self.result_arguments = []  # a list of string representing variables. Ex: "?name"
        self.endpoints = set([])  # SPARQL endpoints where the query should be sent
        self.triples = []  # a list of RDFTriples
        self.limit = u''
        self.query = self.template_query
        self.results = None

    #  -------  Query preparation  -------#
    def add_result_arguments(self, arguments):
        """Add a list of arguments (SPARQL variables) to the SELECT query."""
        map(self.add_result_argument, arguments)

    def add_result_argument(self, argument):
        """Add an argument (SPARQL variable) to the SELECT query.
        For instance, adding argument "?name" will result in a SPARQL
        query having "?name" as part of its variables:
        >>> "SELECT ... ?name ... WHERE {...}"
        """
        self.result_arguments.append(argument)

    def add_query_triples(self, triples):
        """ Add a list of RDF triples to the body of the select query.
        :param triples: A list of RDFtriples
        :return:
        """
        map(self.add_query_triple, triples)

    def add_query_triple(self, triple):
        """ Add an RDF triple to the body of the select query.
        :param triple: A RDFtriple
        :return:
        """
        self.triples.append(triple)
        for p in triple.prefixes:
            self.prefixes.add(p)
            logging.info("Adding triple (%s) to query." %
                         highlight_str(triple, highlight_type='triple'))

    def query_from(self, endpoints):
        """ Add an endpoint to the current query. This query will be send to
        evey listed endpoint. The result will be aggregated.
        For list of supported endpoints, see enum.Endpoints."""
        if type(endpoints) == Endpoint:
            self.endpoints.add(endpoints)
        else:
            for endpoint in endpoints:
                if type(endpoint) == Endpoint:
                    self.endpoints.add(endpoint)
                    logging.info("Adding endpoint %s to query." % highlight_str(endpoint.value))
                else:
                    raise QueryException(u"Endpoint %s not supported yet." % endpoint)

    def add_prefix(self, prefix):
        """ Convert a string 'abbr: <url>' into a NameSpace, and
        add this NameSpace to the query parameters."""
        abbr, url = decompose_prefix(prefix)
        match = get_consistent_namespace(abbr, url)
        if match:
            self.prefixes.add(match)
            logging.info("Adding prefix %s to query." % highlight_str(match))
        else:
            # Unknown namespace, adding it to the vocabulary
            new_namespace = add_namespace(abbr, url)
            self.prefixes.add(new_namespace)
            logging.info("Adding prefix %s to query." % highlight_str(new_namespace))
        pass

    def add_prefixes(self, prefixes):
        """ Add a list of prefixes of the form ['abbr: <url>']
        to the query parameters."""
        map(self.add_prefix, prefixes)

    def add_filter(self, arguments_names):
        """TODO"""
        # TODO
        raise NotImplementedError

    def add_endpoint(self, endpoint):
        """
        Add the endpoint to the query.
        :param endpoint: the endpoint to add
        :return:
        """
        if type(endpoint) == Endpoint:
            self.endpoints.add(endpoint)
        else:
            raise QueryException(u" Bad endpoint type. Must be an Endpoint, got %i instead." % type(endpoint))

    def add_endpoints(self, endpoints):
        """
        Add the endpoints to the query.
        :param endpoints: the list of endpoints to add
        :return:
        """
        map(self.add_endpoint, endpoints)

    def set_limit(self, limit):
        """ Limits the number of results the query returns."""
        if type(limit) != int:
            raise QueryException(u" Bad limit type. Must be an int, got %i instead." % type(limit))
        elif limit < 1:
            raise QueryException(u" Bad limit value. Must be greater than 0.")

        self.limit = u'LIMIT %i' % limit
        logging.info("Adding limit = %i to query." % limit)

    #  -------  Query Validation & preparation -------#
    def _validate_arguments(self):
        """Check that the query arguments can be used in a valid SPARQL query"""

        # The only mandatory argument to put in our template is the list
        # of rdf triples.
        if not self.triples:
            raise QueryException(
                u"The query can't be instantiated without rdf triples in the WHERE clause")

        # Check prefixes, which is a list of namespace.NameSpace
        if not all(isinstance(p, NameSpace) for p in self.prefixes):
            raise QueryException(
                u"At least one of the prefixes given are NOT of type %s" % NameSpace.__name__)

        # Check that there is at least one endpoint specified. If not, adding the default endpoint.
        if len(self.endpoints) == 0:
            self.endpoints.add(Endpoint.DEFAULT)
            logging.warning("No endpoint were set - Using DEFAULT (%s)" %
                            highlight_str(Endpoint.DEFAULT.value))

    def _querify(self, display_lang=False):
        """ Build a well formed SPARQL query with the given arguments. """

        prefix_strs = (u'PREFIX %s: <%s>' % (prefix.name, prefix.value) for prefix in self.prefixes)

        result_arguments = \
            u'*' if len(self.result_arguments) == 0 \
            else u' '.join(self.result_arguments)

        arguments = {
            u'prefix': u' '.join(prefix_strs),
            u'result_arguments': result_arguments,
            u'triples': u' '.join((t.__str__(display_lang) for t in self.triples)),
            u'limit': self.limit,
        }
        self.query = self.template_query % arguments

    #  -------  Query launch and response processing  -------#
    def _send_requests(self):
        """
        TODO
        :return:
        """
        responses = []

        self._validate_arguments()

        for endpoint in self.endpoints:

            # Depending on the endpoint, queries may be slightly different, especially
            # concerning language information of literals.
            self._querify(display_lang=is_endpoint_multilingual(endpoint))

            logging.info("Sending query %s to endpoint %s ..." % (
                highlight_str(self.query, highlight_type='query'),
                endpoint.value))

            headers = {
                'Accept': 'application/json'
            }
            params = {
                "query": self.query,
                # "default-graph-uri": endpoint.value  # nothing after .xyz
            }
            response = requests.get(endpoint.value, params=params, headers=headers)

            if response.status_code == 200:
                responses.append(response)
            else:
                logging.warning("Query %s returned http code %s when sent to %s." % (
                    highlight_str(self.query, highlight_type='query'),
                    highlight_str(response.status_code),
                    endpoint.value))
        return responses

    def _get_results_from_response(self, http_responses):
        """TODO"""
        return [json.loads(r.content)[u'results'][u'bindings'] for r in http_responses]


    def commit(self):
        """TODO"""
        response = self._send_requests()
        self.results = self._get_results_from_response(response)



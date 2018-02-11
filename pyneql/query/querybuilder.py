#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
querybuilder.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
from pyneql.log.loggingsetup import (
    setup_logging,
    highlight_str
)

from pyneql.utils.utils import (
    QueryException,
    normalize_str
)

from pyneql.utils.endpoints import (
    Endpoint,
    is_endpoint_multilingual
)

from pyneql.utils.namespace import (
    NameSpace,
    decompose_prefix,
    get_consistent_namespace,
    add_namespace
)

from pyneql.utils.wikidataproperties import translate_to_legible_wikidata_properties
import requests
import json

#  ---------------------------------
#        SPARQL queries
#  ---------------------------------


class GenericSPARQLQuery(object):
    """A generic SPARQL 'select' query builder.
     It is used to build SPARQL queries iteratively."""

    setup_logging()
    template_query = u'%(prefix)s SELECT DISTINCT %(result_arguments)s WHERE { %(triples)s } %(limit)s'

    def __init__(self):
        self.prefixes = set([])  # a set of vocabulary.prefixes
        self.languages = set([])  # a set of enum.LanguagesIso6391 the query literals should be in (and retrieve)
        self.result_arguments = []  # a list of string representing variables. Ex: "?name"
        self.endpoints = set([])  # SPARQL endpoints where the query should be sent
        self.triples = []  # a list of RDFTriples
        self.alternate_triples = []  # a list of sets of alternative triples
        self.limit = 'LIMIT 1500'  # Arbitrary high limit in order to avoid querying the whole DB
        self.queries = {}
        self.results = []

    #  -------  Query preparation  -------#
    def add_result_arguments(self, arguments):
        """Add a list of arguments (SPARQL variables) to the SELECT query.

        :param arguments: A list of string representing SPARQL variables"""
        map(self.add_result_argument, arguments)

    def add_result_argument(self, argument):
        """Add an argument (SPARQL variable) to the SELECT query.
        For instance, adding argument "?name" will result in a SPARQL
        query having "?name" as part of its variables:

        ``SELECT ... ?name ... WHERE {...}``

        :param argument: A string representing a SPARQL variable
        """
        self.result_arguments.append(argument)

    def add_query_triples(self, triples):
        """ Add a list of RDF triples to the body of the select query.

        :param triples: A list of :class:`RDFtriple`
        """
        map(self.add_query_triple, triples)

    def add_query_triple(self, triple):
        """ Add an RDF triple to the body of the select query.

        :param triple: A :class:`RDFtriple`
        """
        self.triples.append(triple)
        for p in triple.prefixes:
            self.prefixes.add(p)

        self.languages.add(triple.language)
        logging.debug("Adding triple (%s) to query." % highlight_str(triple, highlight_type='triple'))

    def add_query_alternative_triples(self, triples_set):
        """
        Add a set of RDFtriples to the query using SPARQL 'UNION' in order to
        express alternatives.
        ``{ x } UNION { y }`` will match either x or y, or both.
        .. seealso:: https://www.w3.org/TR/rdf-sparql-query/ for more details.

        :param triples_set: A set of :class:`RDFtriple`
        """
        self.alternate_triples.append(triples_set)
        for triple in triples_set:
            for p in triple.prefixes:
                self.prefixes.add(p)
            self.languages.add(triple.language)
            logging.debug("Adding alternate triple (%s) to query." %
                          highlight_str(triple, highlight_type='triple'))


    def add_prefix(self, prefix):
        """ Convert a string ``abbr: <url>`` into a :class:`NameSpace`, and
        add this NameSpace to the query parameters.

        :param prefix: a string representing a RDF prefix"""
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
        to the query parameters.

        :param prefix: a list of strings representing RDF prefixes

        """
        map(self.add_prefix, prefixes)

    def add_filter(self, arguments_names):
        """Not Implemented Yet: Add a filter clause to the SPARQL query. TODO
        """
        # TODO
        raise NotImplementedError

    def add_endpoint(self, endpoint):
        """
        Add an :class:`Endpoint` to the current query. This query will be send to
        evey listed endpoint. The result will be aggregated.
        For list of supported endpoints, see enum.Endpoints

        :param endpoint: the endpoint to add
        """
        if type(endpoint) == Endpoint:
            self.endpoints.add(endpoint)
        else:
            raise QueryException(u" Bad endpoint type. Must be an Endpoint, got %s instead." % type(endpoint))

    def add_endpoints(self, endpoints):
        """
        Add a list of :class:`Endpoints` to the query.

        :param endpoints: the list of :class:`Endpoints` to add

        """
        map(self.add_endpoint, endpoints)

    def set_limit(self, limit):
        """ Limits the number of results the query returns.

        :param limit: int (the limit of query results)
        """
        if type(limit) != int:
            raise QueryException(u" Bad limit type. Must be an int, got %s instead." % type(limit))
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

    def _querify(self, endpoint=Endpoint.DEFAULT):
        """ Build a well formed SPARQL query with the given arguments for all the endpoints.

        :param endpoint: The :class:`Endpoint` to which the query will be sent"""

        prefix_strs = (u'PREFIX %s: <%s>' % (prefix.name, prefix.value) for prefix in self.prefixes)

        result_arguments = \
            u'*' if len(self.result_arguments) == 0 \
            else u' '.join(self.result_arguments)

        arguments = {
            u'prefix': u' '.join(prefix_strs),
            u'result_arguments': result_arguments,
            u'triples': u' '.join((
                t.__str__(is_endpoint_multilingual(endpoint))
                for t in self.triples
                if endpoint not in t.forbidden_endpoints)),
            u'limit': self.limit,
        }

        # Adding alternative triples
        for triples_set in self.alternate_triples:
            query_chunk = u' UNION '.join([
                u'{ %s }' % t.__str__(is_endpoint_multilingual(endpoint)).strip('.')
                for t in triples_set])+u' . '
            arguments[u'triples'] = u'%s %s' % (arguments[u'triples'], query_chunk)

        # Wikidata specific text to get the item as well as its label
        if endpoint == Endpoint.wikidata:
            arguments[u'triples'] = \
                u'SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],%s". } %s' % (
                    u', '.join([l.value for l in self.languages]),
                    arguments[u'triples'])
        self.queries[endpoint] = self.template_query % arguments

    def reset_queries(self):
        """
        Resets the queries already constructed.

        """
        self.queries = {}

    #  -------  Query launch and response processing  -------#
    def _send_requests(self):
        """
        Send the current query to the SPARQL endpoints declared in self.endpoints.

        :return: the list of http responses for the current query fore each SPARQL endpoint.
        """
        responses = []

        self._validate_arguments()

        for endpoint in self.endpoints:

            # Depending on the endpoint, queries may be slightly different, especially
            # concerning language information of literals.
            self._querify(endpoint)
            if not self.queries.get(endpoint, False):
                raise QueryException(u"No query was generated for endpoint %s." % str(endpoint))

            logging.debug("Sending query %s to endpoint %s ..." % (
                highlight_str(self.queries.get(endpoint, "{}"), highlight_type='query'),
                endpoint.value))

            headers = {
                'Accept': 'application/json'
            }
            params = {
                "query": self.queries.get(endpoint, "{}"),
                # "default-graph-uri": endpoint.value  # nothing after .xyz
            }



            response = requests.post(endpoint.value, params=params, headers=headers)
            # using POST instead of GET because it is slightly more efficient for big
            # queries (POST queries are not cached)

            if response.status_code == 200:
                responses.append(response)
            else:
                logging.warning("Query %s returned http code %s when sent to %s." % (
                    highlight_str(self.queries.get(endpoint, "{}"), highlight_type='query'),
                    highlight_str(response.status_code),
                    endpoint.value))
        return responses

    def _normalize_result(self, result):

        result = translate_to_legible_wikidata_properties(result)
        return normalize_str(result)

    def _compute_results_from_response(self, http_responses):
        """Given the http response corresponding to self.query, this method
        stores in self.results the list of list of subject, predicates and object
        (which were arguments of the query), associated to their values.

        >>>pprint.pprint(self.results)
        >>>[
        >>>  [ (u'subj', u'http://fr.dbpedia.org/resource/Marguerite_Duras'),
        >>>    (u'pred', u'http://rdvocab.info/ElementsGr2/placeOfBirth'),
        >>>    (u'obj', u'Gia Dinh (Vietnam)')
        >>>   ],
        >>>  [ (u'subj', u'http://fr.dbpedia.org/resource/Marguerite_Duras'),
        >>>    (u'pred', u'http://rdvocab.info/ElementsGr2/placeOfDeath'),
        >>>    (u'obj', u'Paris')
        >>>  ]
        >>>]

        :param http_responses: an HTTP response
        """

        results = [json.loads(r.content)[u'results'][u'bindings'] for r in http_responses]
        for result in results:
            self.results += map(
                lambda d: [
                    (k, self._normalize_result(v[u'value']))
                    for k, v
                    in d.items()
                ],
                result)


    def commit(self):
        """Send the current query to the specified SPARQL endpoints and stores the
        query results in the results attribute."""
        response = self._send_requests()
        self._compute_results_from_response(response)

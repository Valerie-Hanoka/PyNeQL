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
    LanguagesIso6391 as Lang,
    Endpoint
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
        self.result_arguments = ["*"]  # a list of string representing variables. Ex: "?name"
        self.endpoints = set([])  # SPARQL endpoints where the query should be sent
        self.triples = []  # a list of RDFTriples
        self.limit = u''
        self.query = self.template_query
        self.results = None

    #  -------  Query preparation  -------#
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
                else:
                    raise QueryException(u"Endpoint %s not supported yet." % endpoint)

    def add_prefix(self, prefix):
        """ Convert a string 'abbr: <url>' into a NameSpace, and
        add this NameSpace to the query parameters."""
        abbr, url = decompose_prefix(prefix)
        match = get_consistent_namespace(abbr, url)
        if match:
            self.prefixes.add(match)
        else:
            # Unknown namespace, adding it to the vocabulary
            new_namespace = add_namespace(abbr, url)
            self.prefixes.add(new_namespace)
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

        self.limit = u'LIMIT %i' %limit

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

    def _querify(self):
        """ Build a well formed SPARQL query with the given arguments. """

        self._validate_arguments()
        prefix_strs = (u'PREFIX %s: <%s>' % (prefix.name, prefix.value) for prefix in self.prefixes)
        arguments = {
            u'prefix': u' '.join(prefix_strs),
            u'result_arguments': u'*',  # TODO
            u'triples': u' '.join((str(t) for t in self.triples)),
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
        for endpoint in self.endpoints:
            logging.info("Sending query %s to endpoint %s ..." % (
                highlight_str(self.query, highlight_type='query'),
                endpoint.value))
            headers = {
                'Accept': 'application/json'
            }
            params = {
                "query": self.query,
                # "default-graph-uri": endpoint.value  # TODO nothing after .xyz
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
        final_results = {}
        responses = [json.loads(r.content)[u'results'][u'bindings'] for r in http_responses]
        for raw_results in responses:
            for raw_result in raw_results:
                for k, v in raw_result.iteritems():
                    new_v = final_results.get(k, set([]))
                    new_v.add(v[u'value'])
                    final_results[k] = new_v
        return final_results

    def commit(self):
        """TODO"""
        self._querify()
        response = self._send_requests()
        self.results = self._get_results_from_response(response)


class PersonQuery(GenericSPARQLQuery):
    """
    TODO
    """

    def __init__(self,
                 full_name=None,
                 last_name=None,
                 first_name=None,
                 birth_date=None,
                 death_date=None,
                 query_language=Lang.DEFAULT
                 ):
        """TODO"""
        self.full_name = full_name
        self.last_name = last_name,
        self.first_name = first_name,
        self.birth_date = birth_date,
        self.death_date = death_date,
        self.query_language = query_language

    def _querify(self):
        """"""
        # TODO constuire les triplets adéquats avec les prédicats correspondants
        # à des éléments du vocabulaire

# PREFIX dbpprop: <http://dbpedia.org/property/>
# select distinct ?x ?y ?z ?z2 where {
#   ?x rdf:type foaf:Person .
#   ?x ?first_name "Benny"@en .
#   ?x ?last_name "Goodman"@en .
#   ?x ?y ?z .
#   ?z rdfs:label ?z2 .
# }


class PeriodQuery(GenericSPARQLQuery):
    """
    TODO: Time and period
    SELECT * WHERE
    { ?x
    rdfs:label
    "Renaissance" @ fr; ?y ?z.}
    pass
    """



class LocationQuery(GenericSPARQLQuery):
    """
    TODO: a place
    """

    options = {
        'query_term': "Max Power",
        'query_term_lang': Lang.DEFAULT,
    }

class MasterPieceQuery(GenericSPARQLQuery):
    """
    TODO: une oeuvre
    """

    options = {
        'query_term': "Max Power",
        'query_term_lang': Lang.DEFAULT,
    }
    # Dublin core



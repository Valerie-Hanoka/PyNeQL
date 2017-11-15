#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
querybuilder.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
import logging.config

from pyneql.rdftriple import RDFTriple
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

logging.getLogger(__name__).addHandler(logging.NullHandler())


#---------------------------------
#        SPARQL queries
#---------------------------------

class GenericSPARQLQuery():
    """A generic SPARQL 'select' query builder.
     It is used to build queries iteratively."""

    template_query = """
    {prefix}
    SELECT {result_arguments}
    {from_dataset} 
    WHERE {
        {triples}   
    }
    {limit}
    """

    def __init__(self, **kwargs):
        self.prefixes = []  # a list of vocabulary.prefixes
        self.result_arguments = ["*"]  # a list of string representing variables. Ex: "?name"
        self.dataset = []  # Whatever... TODO
        self.triples = []  # a list of RDFTriples
        self.limit = ""  # Whatever... TODO
        self.query = self.template_query

        # for key in kwargs:
        #     if getattr(self, key):
        #         setattr(self, key, kwargs[key])
        #     else:
        #         logging.warning("Parameter %s can't be set for object %s."
        #                         %(key, self.__class__.__name__))

    #-------  Query preparation  -------#
    def add_query_triple(self, **triple):
        """ Add an RDF triple to the body of the select query."""
        index = len(self.triples)
        self.triples.append(
            RDFTriple(
                subject=triple.get("subject", "?s_%i" % index),
                predicate=triple.get("predicate", "?p_%i" % index),
                object=triple.get("object", "?o_%i" % index),
                prefixes=triple.get("prefixes", None))
        )

    def query_from(self, endpoints):
        """ Add an endpoint to the current query. This query will be send to
        evey listed endpoint. The result will be aggregated.
        For list of supported endpoints, see enum.Endpoints."""
        if type(endpoints) == Endpoint:
            self.dataset.append(endpoints)
        else:
            for endpoint in endpoints:
                if type(endpoint) == Endpoint:
                    self.dataset.append(endpoint)
                else:
                    raise QueryException("Endpoint %s not supported yet." % endpoint)

    def add_prefix(self, prefix):
        """ Convert a string 'abbr: <url>' into a NameSpace, and
        add this NameSpace to the query parameters."""
        abbr, url = decompose_prefix(prefix)
        match = get_consistent_namespace(abbr, url)
        if match:
            self.prefixes.append(match)
        else:
            # Unknown namespace, adding it to the vocabulary
            new_namespace = add_namespace(abbr, url)
            self.prefixes.append(new_namespace)
        pass

    def add_prefixes(self, prefixes):
        """ Add a list of prefixes of the form ['abbr: <url>']
        to the query parameters."""
        map(self.add_prefix, prefixes)

    def add_filter(self, arguments_names):
        """TODO"""
        # TODO
        pass

    def set_limit(self, limit):
        """ Limits the number of results the query returns."""
        if type(limit) != int:
            raise QueryException(" Bad limit type. Must be an int, got %i instead." % type(limit))
        self.limit = limit

    #-------  Query Validation & preparation -------#

    def _validate_arguments(self):
        """Check that the query arguments can be used in a valid SPARQL query"""

        # The only mandatory argument to put in our template is the list
        # of rdf triples.
        if not self.triples:
            raise QueryException(
                "The query can't be instantiated without rdf triples in the WHERE clause")

        # Check prefixes, which is a list of namespace.NameSpace
        if not all(isinstance(p, NameSpace) for p in self.prefixes):
            raise QueryException(
                "At least one of the prefixes given are NOT of type %s" % NameSpace.__name__)


    def querify(self):
        """ Build a well formed SPARQL query with the given arguments.
        Raise an error if it can't be constructed."""

        self._validate_arguments()
        #self.template_query = self.template_query %


    #-------  Query launch  -------#
    def commit(self):
        """TODO"""
        self._querify





    def __str__(self):
        return self.select_query



class PersonQuery(GenericSPARQLQuery):
    """ Generic Query Builder is the main class in PyNeQL.
    TODO
    """

    options = {
        'query_term': "Max Power",
        'query_term_lang': Lang.DEFAULT,
    }


    def __init__(self, query_term, query_language):
        """TODO"""
        query = "Some stuff"


class PeriodQuery(GenericSPARQLQuery):
    """
    TODO: Time and period
    """
    pass



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



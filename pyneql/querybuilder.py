#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
querybuilder.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
import logging.config

from utils import (
    QueryException,
)

from enum import (
    LanguagesIso6391 as Lang
)

import vocabulary as voc


logging.getLogger(__name__).addHandler(logging.NullHandler())



#---------------------------------
#        SPARQL queries
#---------------------------------

class GenericSPARQLQueryBuilder():
    """A generic SPARQL 'select' query builder.
     It is used to build queries iteratively."""

    prefixes = []          # a list of vocabulary.prefixes
    result_arguments = []  # a list of string.  Ex: "?name"
    dataset = []
    triples = [] # a list of 3-uplets
    limit = ""

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
        """ Stores the arguments of the query to build."""
        for key in kwargs:
            if getattr(self, key):
                setattr(self, key, kwargs[key])
            else:
                logging.warning("Parameter %s can't be set for object %s."
                                %(key, self.__class__.__name__))

    def _validate_arguments(self):
        """Check that the query arguments can be used in a valid SPARQL query"""

        # The only mandatory argument to get in our template is the list
        # of rdf triples.
        if not self.triples:
            raise QueryException(
                "The query can't be instantiated without rdf triples in the WHERE clause")

        # Check prefixes, which is a list of vocabulary.prefixes
        if not all(isinstance(p, voc.NameSpace) for p in self.prefixes):
            raise QueryException(
                "At least one of the prefixes given are not of type vocabulary.NameSpace")

        # Check triples and arguments
        for (s, p, o) in self.triples:
            #TODO
            pass




    def querify(self):
        """ Build a well formed SPARQL query with the given arguments.
        Raise an error if it can't be constructed."""

        self._validate_arguments()
        #self.template_query = self.template_query %




    def __str__(self):
        return self.select_query


    select_query = """
    {prefix}
    SELECT {result_arguments}
    FROM {dataset} 
    WHERE {
        {triplets}   
    }
    {limit}
    """




class PersonQueryBuilder(GenericSPARQLQueryBuilder):
    """ Generic Query Builder is the main class in PyNeQL.
    TODO
    """

    options = {
        'query_term': "Simone de Beauvoir",
        'query_term_lang': Lang.DEFAULT,
    }


    def __init__(self, query_term, query_language):
        """TODO"""
        query = """
    SELECT * WHERE {
        ?entity1 ?x "{term}"@{lang} .
        ?entity1 ?y ?entity2 .
}    
    """








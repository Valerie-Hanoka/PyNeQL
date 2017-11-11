#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
querybuilder.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
import logging.config

from utils import (
    NameSpaceException,
    QueryException,
    normalize_str
)

from enum import (
    LanguagesIso6391 as Lang
)


import vocabulary as voc
import re


logging.getLogger(__name__).addHandler(logging.NullHandler())

#---------------------------------
#        RDF formalism
#---------------------------------

RE_PREFIX_SEPARATOR = re.compile('.*/|#')
RE_NAMESPACE_CHECKER = re.compile(
    '^\s*(?P<abbr>\w+)\s*:\s*<(?P<ns>http://[^>\s]+)>[\s\.]*$')


class RDFTripletBuilder:
    """Creates an RDF triple that can be used for querying in a select statement."""

    prefixes = []
    subject = u"?s"
    predicate = u"?p"
    object = u"?o"

    def __init__(self,
                 subject=u"?s",
                 predicate=u"?p",
                 object=u"?o",
                 prefixes=None):

        self.prefixes = []
        prefixes = prefixes or []
        logging.debug("Initialisation of triplet:\n(%s %s %s)" %
                      (self.subject, self.predicate, self.object))

        logging.debug("Prefixes: %s" % self.prefixes)
        self.add_prefixes(prefixes)

        # If variable is not instantiated, we use its name as a variable name
        if subject:
            self.subject = self._extract_prefix_from_rdf_element(subject)
        if predicate:
            self.predicate = self._extract_prefix_from_rdf_element(predicate)
        if object:
            self.object = self._extract_prefix_from_rdf_element(object)

        logging.debug("Prefixes: %s" % self.prefixes)


    def _extract_prefix_from_rdf_element(self, element):
        """
        Element is one part of an rdf triple.

        This element can be of the form:
            1- '<http://purl.org/dc/elements/1.1/title>'
            2- 'dc:title'
            3- '?anything'

        Case 1: The element contains a namespace. The function replaces it with the
        corresponding prefix if it exists in the vocabulary. If so, the corresponding
        prefix is added to self.prefixes.
        Eg: the predicate <http://purl.org/dc/elements/1.1/title> will become
        dc:title and the prefix vocabulary.NameSpace.dc will be added to self.prefixes.
        If the namespace cannot be identified, then it is just normalized and returned.

        Case 2: The element contains a prefix. If this prefix is already listed in
        self.prefixes, no change is made. If the prefix is not yet in the list,
        we add it if possible (raise a NameSpace Exeption otherwise)

        Case 3: Just normalize the string (spaces, unicode) and return it.

        Return: a normalized string of an rdf triple element
        """

        # Case 1 - The element contains a namespace.
        if element[0] == u'<' and element[-1] == u'>':
            ns_element = element[1:-1]
            matches = RE_PREFIX_SEPARATOR.search(ns_element)
            if matches:
                limit = matches.end()
                pref = ns_element[0:limit]

                # If the namespace is listed in the vocabulary
                # then the element is shortened using the namespace prefix
                # and the prefix is added to the list of prefixes.
                short_prefix = voc.NameSpace(pref)
                if short_prefix:
                    self.add_prefix(short_prefix)
                    element = '%s:%s' % (short_prefix.name, ns_element[limit:])

        # Case 2 - The element contains a prefix
        elif u':' in element:
            pref, elem = element.split(u':')
            known_pref = voc.NameSpace.__members__.get(pref)
            if known_pref:
                self.add_prefix(known_pref)
            else:
                raise  NameSpaceException(
                    "In the standard vocabulary, %s can't be found. "
                    "Without a prior declaration in the prefixes, it can't be used."
                    % known_pref)

        # Case 3 - Other cases
        return normalize_str(element)



    def add_prefixes(self, prefixes):
        """ Add every prefix in the prefixes iterable"""
        map(self.add_prefix, prefixes)

    def add_prefix(self, prefix):
        """ A prefix can be added if it is of the type vocabulary.NameSpace or
        if it is a legal SPARQL query prefix declaration. """

        if not prefix:
            return

        # The prefix is already a vocabulary.NameSpace
        if type(prefix) == voc.NameSpace:
            if prefix not in self.prefixes:
                self.prefixes.append(prefix)

        elif type(prefix) == str:

            # If the prefix is not normalised yet, we normalise it
            is_well_formed = RE_NAMESPACE_CHECKER.match(prefix)
            if is_well_formed:
                abbr = is_well_formed.group("abbr")
                ns = is_well_formed.group("ns")

                # Check if the namespace is present in the vocabulary
                #  and consistent.
                consistent_namespace = voc._get_consistent_namespace(abbr, ns)
                if consistent_namespace:
                    if consistent_namespace not in self.prefixes:
                        self.prefixes.append(consistent_namespace)

                else:
                    # Unknown namespace, adding it to the vocabulary
                    voc.add_namespace(abbr, ns)
                    self.prefixes.append(voc.NameSpace(ns))

            else:
                raise NameSpaceException("Prefix %s is not well formed." % prefix)

        else:
            raise NameSpaceException(
                "Prefix type is not allowed: %s , of type %s. "
                "Should ba a string or a vocabulary.NameSpace " % (prefix, type(prefix)))


    def get_variables(self):
        """ Return the element of the RDF triple which are variables."""
        return [e
                for e in (self.subject, self.object, self.predicate)
                if e[0] == u'?']



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








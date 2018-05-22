#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
rdftriplebuilder is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
from pyneql.log.loggingsetup import (
    setup_logging,
    highlight_str
)

from pyneql.utils.utils import (
    NameSpaceException,
    normalize_str
)

from pyneql.utils.namespace import (
    NameSpace,
    decompose_prefix,
    get_consistent_namespace,
    add_namespace
)

from pyneql.utils.enum import LanguagesIso6391 as Lang

from pyneql.utils.endpoints import Endpoint

import re


#---------------------------------
#        RDF formalism
#---------------------------------
RE_PREFIX_SEPARATOR = re.compile('.*/|#')
RE_IS_STRING_LITERAL = re.compile('^\s*"[^"]*"\s*$')
RE_IS_STRING_A_NUMBER = re.compile('^\s*"[0-9]*"\s*$')

class RDFTriple(object):
    """
    A generic RDF triple representation which can be used for querying in a select statement.
    """
    setup_logging()

    class_counter = 1

    def __init__(self,
                 subject=u'',
                 predicate=u'',
                 object=u'',
                 prefixes=None,             # A list of SPARQL prefixes
                 excluded_endpoints=None,   # A list of endpoints
                 keep_only_endpoints=None,  # A list of endpoints
                 language=Lang.DEFAULT):

        self.id = RDFTriple.class_counter
        RDFTriple.class_counter += 1

        self.subject = u"?s_%i" % RDFTriple.class_counter
        self.predicate = u"?p_%i" % RDFTriple.class_counter
        self.object = u"?o_%i" % RDFTriple.class_counter

        self.prefixes = []
        prefixes = prefixes or []
        self.add_prefixes(prefixes)

        # A triplet can be used to generate many SPARQL queries which
        # will be send to different endpoints. It is thus desirable to tell,
        # for the given triplet, if it is specific to an endpoint or not usable in an
        # endpoint. E.g: wikidata will need specific triplets whereas other endpoints wont.
        self.forbidden_endpoints = set([])
        self.manage_endpoints_information(excluded_endpoints, keep_only_endpoints)

        self.language = language

        # If variable is not instantiated, we use its name as a variable name
        if subject:
            self.subject = self._extract_prefix_from_rdf_element(subject)
        if predicate:
            self.predicate = self._extract_prefix_from_rdf_element(predicate)
        if object:
            self.object = self._extract_prefix_from_rdf_element(object)

        logging.debug("Created triple %s" % highlight_str(self.__str__(), highlight_type='triple'))

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, RDFTriple):
            return (
                    (self.subject == other.subject) and
                    (self.predicate == other.predicate) and
                    (self.object == other.object)
            )
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


    def manage_endpoints_information(self, excluded_endpoints, keep_only_endpoints):
        """ A triplet can be used to generate many SPARQL queries which
        will be send to different endpoints. It is thus desirable to tell,
        for the given triplet, if it is not usable in an endpoint.
        For instance, wikidata may need specific triplets whereas other endpoints wont.

        :Example:

        - ``?x wdt:P31 wd:Q5`` (wikidata specific) may have keep_only_endpoints=[Endpoint.wikidata]
        - ``?Person a foaf:Person`` may have excluded_endpoints=[Endpoint.wikidata]

        :param excluded_endpoints: List of endpoints to which the RDF triple is **not** to be sent
        :param keep_only_endpoints: List of the **only** endpoints to which the RDF triple is to be sent
        """

        # Only one of both is defined
        if bool(excluded_endpoints) ^ bool(keep_only_endpoints):
            if keep_only_endpoints:
                # The keep_only_endpoints tracks the endpoints to which this triplet may be applied.
                self.forbidden_endpoints = set(Endpoint.__members__.values()) - set(keep_only_endpoints)
            else:
                # The excluded_endpoints keeps track of the endpoints we do not wish to submit the current triple.
                # Thus, we exclude them.
                self.forbidden_endpoints = set(excluded_endpoints)

        elif keep_only_endpoints:
            # There is a conflict between 'excluded' and 'keep only' -> 'keep only' defines what should be used
            self.forbidden_endpoints = set(Endpoint.__members__.values()) - set(keep_only_endpoints)

    def __str__(self, with_language=False):
        """
        :return: String version of the triple (without prefixes information)
        """
        if with_language and not isinstance(self.object, int):
            # If the query is prepared for a multilingual endpoint, we must postfix literal text information
            # with its language
            # E.g: '?person ?has_last_name "Obama".' becomes '?person ?has_last_name "Obama"@en.'
            if re.match(RE_IS_STRING_LITERAL, self.object) and not re.match(RE_IS_STRING_A_NUMBER, self.object):
                return u"%s %s %s ." % (
                    self.subject,
                    self.predicate,
                    u'%s@%s' % (self.object, self.language.value)
                )
        return u"%s %s %s ." % (self.subject, self.predicate, self.object)

    def _extract_prefix_from_rdf_element(self, element):
        """ The element can be of the form:
            1- 1789
            2- '<http://purl.org/dc/elements/1.1/title>'
            3- 'dc:title'
            4- '?anything'

        Case 1: Return the unchanged integer

        Case 2: The element contains a namespace. The function replaces it with the
        corresponding prefix if it exists in the vocabulary. If so, the corresponding
        prefix is added to self.prefixes.
        Eg: the predicate <http://purl.org/dc/elements/1.1/title> will become
        dc:title and the prefix vocabulary.NameSpace.dc will be added to self.prefixes.
        If the namespace cannot be identified, then it is just normalized and returned.

        Case 3 - The element is an URL.

        Case 4: The element contains a prefix. If this prefix is already listed in
        self.prefixes, no change is made. If the prefix is not yet in the list,
        we add it if possible (raise a NameSpace Exeption otherwise)

        Other cases: Just normalize the string (spaces, unicode) and return it.

        :param element: One of the 3 element of an RDF triple (subject, object or predicate).
        :return: Normalized string of an rdf triple element if it is a string
        """

        # Case 1 - The element is an integer, and should remain so
        if isinstance(element, int):
            return element

        # Case 2 - The element contains a namespace.
        if element[0] == u'<' and element[-1] == u'>':
            ns_element = element[1:-1]
            matches = RE_PREFIX_SEPARATOR.search(ns_element)
            if matches:
                limit = matches.end()
                pref = ns_element[0:limit]

                # If the namespace is listed in the vocabulary
                # then the element is shortened using the namespace prefix
                # and the prefix is added to the list of prefixes.
                short_prefix = NameSpace(pref)
                if short_prefix:
                    self.add_prefix(short_prefix)
                    element = u'%s:%s' % (short_prefix.name, ns_element[limit:])

        # Case 3 - The element is an URL.
        elif element[0:7] == 'http://':
            return u'<%s>' % element

        # Case 4 - The element contains a prefix
        elif u':' in element:
            pref, elem = element.split(u':')
            known_pref = NameSpace.__members__.get(pref)

            if known_pref:
                # The prefix is known. Then we add it.
                self.add_prefix(known_pref)

                # Enums labels with duplicate values are turned into aliases for the first such label.
                # This can lead to Namespaces prefix differences in the prefix list and the element.
                # In order to avoid this unwanted behavior, we transform the element prefix to its main alias.
                # E.g: element "dbpedia_owl:birthDate" will be transformed to "dbo:birthDate" (known_pref.name).

                if not known_pref == pref:
                    # Duplicate names in NameSpace => using the main alias for the duplicate namespaces.
                    element = element.replace(u'%s:' % pref, u'%s:' % known_pref.name)
            else:
                raise NameSpaceException(
                    u"In the standard vocabulary, %s can't be found. "
                    u"Without a prior declaration in the prefixes, it can't be used."
                    % known_pref)
        # Other cases
        return normalize_str(element)



    def add_prefixes(self, prefixes):
        """ Add every prefix in the prefixes iterable"""
        for prefix in prefixes:
            self.add_prefix(prefix)

    def add_prefix(self, prefix):
        """ A prefix can be added if it is of the type vocabulary.NameSpace or
        if it is a legal SPARQL query prefix declaration.
        >>> my_triple = RDFTriple(object="foo")
        >>> my_triple.add_prefix(NameSpace.dawgt)
        >>> my_triple.add_prefix("barbarbar: <http://bar.org/bar/bar/> .")

        """

        if not prefix:
            raise NameSpaceException(u"Prefix issue: can't add undefined prefix.")

        # The prefix is already a vocabulary.NameSpace
        if isinstance(prefix, NameSpace):
            if prefix not in self.prefixes:
                self.prefixes.append(prefix)

        elif isinstance(prefix, str) or isinstance(prefix, unicode):

            # If the prefix is not normalised yet, we normalise it
            abbr, ns = decompose_prefix(prefix)

            # Check if the namespace is present in the vocabulary
            #  and consistent.
            consistent_namespace = get_consistent_namespace(abbr, ns)
            if consistent_namespace:
                if consistent_namespace not in self.prefixes:
                    self.prefixes.append(consistent_namespace)

            else:
                # Unknown namespace, adding it to the vocabulary
                new_namespace = add_namespace(abbr, ns)
                self.prefixes.append(new_namespace)
                logging.info("Adding prefix %s to NameSpaces vocabulary." % new_namespace)

        else:
            raise NameSpaceException(
                u"Prefix type is not allowed: %s , of type %s. "
                u"Should ba a string or a vocabulary.NameSpace " % (prefix, type(prefix)))


    def get_variables(self):
        """
        Given a well-formed SPARQL query, returns its variables.
        :return: the elements of the RDF triple which are variables.
        """
        return [e for e in (self.subject, self.object, self.predicate) if e[0] == u'?']




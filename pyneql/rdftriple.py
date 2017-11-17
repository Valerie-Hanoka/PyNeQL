#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
rdftriplebuilder is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
from loggingsetup import (
    setup_logging,
    highlight_str
)

from utils import (
    NameSpaceException,
    normalize_str
)

from namespace import (
    NameSpace,
    decompose_prefix,
    get_consistent_namespace,
    add_namespace
)
import re


#---------------------------------
#        RDF formalism
#---------------------------------
RE_PREFIX_SEPARATOR = re.compile('.*/|#')

class RDFTriple(object):
    """
    A generic RDF triple that can be used for querying in a select statement.
    """
    setup_logging()

    class_counter = 1

    def __init__(self,
                 subject=u'',
                 predicate=u'',
                 object=u'',
                 prefixes=None):

        self.id = RDFTriple.class_counter
        RDFTriple.class_counter += 1

        self.prefixes = []
        self.subject = u"?s_%i" % RDFTriple.class_counter
        self.predicate = u"?p_%i" % RDFTriple.class_counter
        self.object = u"?o_%i" % RDFTriple.class_counter
        prefixes = prefixes or []
        self.add_prefixes(prefixes)

        # If variable is not instantiated, we use its name as a variable name
        if subject:
            self.subject = self._extract_prefix_from_rdf_element(subject)
        if predicate:
            self.predicate = self._extract_prefix_from_rdf_element(predicate)
        if object:
            self.object = self._extract_prefix_from_rdf_element(object)

        logging.info("Created triple %s" % highlight_str(self.__str__(), highlight_type='triple'))

    def __str__(self):
        """
        :return: String version of the triple (without prefixes information)
        """
        return u"%s %s %s ." % (self.subject, self.predicate, self.object)

    def _extract_prefix_from_rdf_element(self, element):
        """ The element can be of the form:
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

        :param element: One of the 3 element of an RDF triple (subject, object or predicate).
        :return: Normalized string of an rdf triple element
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
                short_prefix = NameSpace(pref)
                if short_prefix:
                    self.add_prefix(short_prefix)
                    element = u'%s:%s' % (short_prefix.name, ns_element[limit:])

        # Case 2 - The element contains a prefix
        elif u':' in element:
            pref, elem = element.split(u':')
            known_pref = NameSpace.__members__.get(pref)
            if known_pref:
                self.add_prefix(known_pref)
            else:
                raise NameSpaceException(
                    u"In the standard vocabulary, %s can't be found. "
                    u"Without a prior declaration in the prefixes, it can't be used."
                    % known_pref)

        # Other cases
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
        if type(prefix) == NameSpace:
            if prefix not in self.prefixes:
                self.prefixes.append(prefix)

        elif type(prefix) == str:

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

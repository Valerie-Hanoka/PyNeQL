#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
thing.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from pyneql.log.loggingsetup import (
    setup_logging,
)

from pyneql.query.querybuilder import GenericSPARQLQuery
from pyneql.query.rdftriple import RDFTriple
from pyneql.utils.vocabulary import (
    rdf_types,
    attributes as voc_attributes
)

from pyneql.utils.enum import (
    LanguagesIso6391 as Lang,
)

from pyneql.utils.namespace import get_shortened_uri
from pyneql.utils.utils import (
    QueryException,
    merge_two_dicts_in_sets
)


class Thing(object):
    """
    A semantic representation of a Thing, retrieved from the Semantic Web.
    """

    setup_logging()

    # Query
    query_builder = None
    endpoints = None

    # Results
    attributes = None

    # Implementation convention
    # Elements which will be used to construct the query
    # for something more specific than a Thing
    # bust begin with "has_".
    has_label = None

    def __init__(
            self,
            query_language=Lang.DEFAULT,
            label=None,
            endpoints=None,  # SPARQL endpoints where the query should be sent
            class_name=u'Thing'
            ):

        if not isinstance(query_language, Lang):
            raise QueryException("The language of the query must be of type enum.LanguagesIso6391.")

        self.has_label = label

        self.class_name = class_name
        self.rdf_types = rdf_types[class_name]
        self.voc_attributes = voc_attributes[class_name]

        self.args = {
            'subject': u'?%s' % class_name,
            'predicate': u'?pred',
            'object': u'?obj'
        }

        self.query_builder = GenericSPARQLQuery()
        self.query_language = query_language

        self.endpoints = endpoints if endpoints else set([])
        self.attributes = {}

    def add_query_endpoints(self, endpoints):
        map(self.add_query_endpoint, endpoints)

    def add_query_endpoint(self, endpoint):
        self.endpoints.add(endpoint)

    def _build_query(self, strict_mode=True):
        """
        Updates the query_builder of the thing.
        There are two modes available for this query: strict and non strict.
        Let's take an example:
        We are looking for a Thing whose attribute 'foo' is "አዲስ አበባ".
        • Non strict mode will have its query restrained to elements satisfying
          the triplet '?Thing ?has_foo "አዲስ አበባ".'.
          The predicate is left undetermined ("?has_foo" is a variable).
        • In strict mode, we are strict about the types of predicates of the triplet.
          For the current class ('Thing'), those predicates will be listed in
          self.voc_attributes['has_foo'] and combined in the SPARQL query:
          "[…]{ ?Thing foo:bar "አዲስ አበባ"  } UNION { ?Thing foo:baz "አዲስ አበባ"  }.[…]

        :param strict_mode: True (default) if strict_mode is enabled, False otherwise
        :return:
        """

        self.query_builder.reset_queries()
        # Restricting the query to elements of the current type
        # This will build a query with
        to_unite = set([])
        for class_type in self.rdf_types:
            to_unite.add(
                RDFTriple(subject=self.args['subject'],
                          predicate=u'a',
                          object=class_type,
                          language=self.query_language
                          )
            )
        self.query_builder.add_query_alternative_triples(to_unite)

        # Adding query delimiters, that are the parameters given for query
        # (i.e stored in the instance variables begining with "has_").

        # The query will be generated according to the class variables beginning with 'has_'.
        entities_names = [e for e in self.__dict__.keys() if e.startswith('has_') and self.__dict__.get(e, False)]
        for entity_name in entities_names:
            entity_value = self.__dict__.get(entity_name, None)
            # The instance has an instantiated value for a 'has_…' variable. This value will be the
            # object of an RDF triplet.
            if entity_value:
                try:
                    # For dates elements, the triplet literal must be formatted without quotes
                    obj = int(entity_value)
                except ValueError:
                    obj = u'"%s"' % entity_value
            else:
                # If no value was specified, the object will be a variable in the SPARQL query
                obj = u'?%s' % entity_name
            pred = u'?%s' % entity_name

            if strict_mode and entity_name in self.voc_attributes:
                to_unite = set([])
                for attribute_name in self.voc_attributes[entity_name]:
                    to_unite.add(
                        RDFTriple(
                            subject=self.args['subject'],
                            predicate=attribute_name,
                            object=obj,
                            language=self.query_language
                        )
                    )
                self.query_builder.add_query_alternative_triples(to_unite)

            else:
                self.query_builder.add_query_triple(
                    RDFTriple(
                        subject=self.args['subject'],
                        predicate=pred,
                        object=obj,
                        language=self.query_language
                    )
                )

        # Fetching everything about that Thing
        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=self.args['predicate'],
                object=self.args['object'],
                language=self.query_language
            )
        )

    def query(self, strict_mode=True):

        self._build_query(strict_mode)
        self.query_builder.add_endpoints(self.endpoints)
        wanna_know = [self.args['subject'], self.args['predicate'], self.args['object']]
        self.query_builder.add_result_arguments(wanna_know)
        self.query_builder.commit()
        self._process_results()

    def _process_results(self):
        """Given the result of a SPARQL query to find a Thing,
        this creates a Thing with all the information gathered."""

        values_to_check = {v: e for e, v in self.__dict__.items() if e.startswith('has_') and self.__dict__.get(e, False)}
        things = {}

        for result in self.query_builder.results:

            dict_results = {arg_name: get_shortened_uri(arg_value) for (arg_name, arg_value) in result}
            thing = dict_results.pop(self.args['subject'][1:], None)

            # Checking that it is the thing we are looking for
            if dict_results[self.args['object'][1:]] in values_to_check:
                value = dict_results[self.args['object'][1:]]
                properties = self.voc_attributes.get(values_to_check[value], False)
                if properties and dict_results[self.args['predicate'][1:]] in properties:
                    things[thing]["validated"] = 1

            shortened_result = {dict_results[u'pred']: dict_results[u'obj']}
            things[thing] = merge_two_dicts_in_sets(things.get(thing, {}), shortened_result)

        # Wikimedia... (╯°□°）╯︵ ┻━┻ Accepting wikimedia elements that correspond to an entity because
        # what we will have TODO is to filter them properly.
        unfiltered_wikimedia_things = [t for t in things.keys() if 'wd:' in t and not t == u'wd:Q12949604']
        for unfiltered_wikimedia_thing in unfiltered_wikimedia_things:
            things[unfiltered_wikimedia_thing]["validated"] = 1

        # Removing wrong things and adding the attributes of the correct thing
        for thing, thing_attribute in things.items():
            if not thing_attribute.get('validated', False):
                things.pop(thing)
            else:
                self.attributes = merge_two_dicts_in_sets(self.attributes, {u'owl:sameAs': thing})
                self.attributes = merge_two_dicts_in_sets(self.attributes, {u'skos:exactMatch': thing}) # Identity
                self.attributes = merge_two_dicts_in_sets(self.attributes, thing_attribute)


    def get_external_ids(self):
        """
        Get the external ids of the Thing.
        """
        raise NotImplementedError('Subclasses must override get_external_ids()!')

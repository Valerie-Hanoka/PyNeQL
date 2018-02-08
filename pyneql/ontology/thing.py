#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
thing.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
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

from pyneql.utils.utils import normalize_str

from functools import reduce
import itertools


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
    has_url = None

    def __init__(
            self,
            query_language=Lang.DEFAULT,
            label=None,
            url=None,
            endpoints=None,  # SPARQL endpoints where the query should be sent
            class_name=u'Thing'
            ):

        if not isinstance(query_language, Lang):
            raise QueryException("The language of the query must be of type enum.LanguagesIso6391.")

        self.has_label = label
        self.has_url = url

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

    # --------------------------------------- #
    #           QUERIES PREPARATION
    # --------------------------------------- #

    # --- Queries parameters: endpoints --- #

    def add_query_endpoints(self, endpoints):
        """This function allows to add a list of endpoints to which the Thing queries will be sent.
        :param endpoints: A list of endpoints we wish to query for the construction of the current Thing.
        """
        map(self.add_query_endpoint, endpoints)

    def add_query_endpoint(self, endpoint):
        """
        Any ontology object (here, a Thing) will be constructed through
        SPARQL queries send to some specified SPARQL endpoints.
        This function allows to add a single endpoint for the query.
        :param endpoint: An endpoint we wish to query for the construction of the current Thing.
        """
        self.endpoints.add(endpoint)

    # --- Queries preparation --- #

    def _build_query(self, check_type=True, strict_mode=False):
        """
        In order to retrieve an ontology object (Thing, Person, Location,...) from the
        semantic web, a SPARQL query will be sent to all the specified SPARQL endpoints.
        This function builds the queries to find the current objects in all
        the endpoints, depending on some query options.
        The queries options relies on the dictionaries contained in pyneql/utils/vocabulary.py.

        :param check_type: Boolean. Check the type of the object (e.g: Book, Person, Location,…)
        directly in the SPARQL queries.
        If True, the restriction of the object's type is done in the query.
        For instance, if the object is a Book, activating strict_mode will build queries where the object
        to find (?Book) is constrained by an union of RDF triples checking that ?Book is a Book:
        "[…] { ?Book a fabio:Book  } UNION […] UNION { ?Book a schemaorg:Book  } .

        :param strict_mode: Boolean. Check the type of the object's attributes (e.g: label, first name,…)
        directly in the SPARQL queries.
        If True, the predicates of the triplet whose values are instantiated will have their types checked
        against the allowed types listed in self.voc_attributes.
        Let's take an example:
        We are looking for a Thing whose attribute 'label' is "አዲስ አበባ".
        • Non strict mode will have its query restrained to elements satisfying
          the triplet '?Thing ?has_label "አዲስ አበባ".'.
          The predicate is left undetermined ("?has_label" is a variable).
        • In strict mode, we are strict about the types of predicates of the triplet.
          For the current class ('Thing'), those predicates will be listed in
          self.voc_attributes['has_label'] and combined in the SPARQL query.
          Here, for the example, we set 'has_label' allowed the RDF predicates 'rdfs:label' and u'wdt:P1813'.
          >>> print(self.voc_attributes['has_label'])
          >>> [u'rdfs:label', u'wdt:P1813']
          So in strict_mode, the query will be constrained to:
          "[…]{ ?Thing rdfs:label "አዲስ አበባ"  } UNION { ?Thing wdt:P1813 "አዲስ አበባ"  }.[…]
        """

        self.query_builder.reset_queries()

        # The query will be generated according to the class variables beginning with 'has_'.
        entities_names = [e for e in self.__dict__.keys() if e.startswith('has_') and self.__dict__.get(e, None)]

        if 'has_url' in entities_names:
            # If we already have an url to query, the object we are looking for is unambiguous.
            # We thus do not need to build a specific query to find it.
            wanna_know = [self.args['predicate'], self.args['object']]
            self._build_url_query()
        else:
            # we have to find the thing using other clues (as label, names, dates,…)
            wanna_know = [self.args['subject'], self.args['predicate'], self.args['object']]
            self._build_standard_query(entities_names, check_type=check_type, strict_mode=strict_mode)

        self.query_builder.add_result_arguments(wanna_know)

    def _build_url_query(self):
        """If the current object is already identified by an URL/URI, we can unambiguously query it.
        The URL becomes the subject of our RDF triple.
        """
        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.has_url,
                predicate=self.args['predicate'],
                object=self.args['object'],
                language=self.query_language
            )
        )

    def _build_standard_query(self, entities_names, check_type=True, strict_mode=False):
        """
        Updates the query_builder of the object.
        The queries options relies on the dictionaries contained in pyneql/utils/vocabulary.py.

        :param check_type: Boolean. Check the type of the object (e.g: Book, Person, Location,…)
        directly in the SPARQL queries.
        If True, the restriction of the object's type is done in the query.
        For instance, if the object is a Book, activating strict_mode will build queries where the object
        to find (?Book) is constrained by an union of RDF triples checking that ?Book is a Book:
        "[…] { ?Book a fabio:Book  } UNION […] UNION { ?Book a schemaorg:Book  } .

        :param strict_mode: Boolean. Check the type of the object's attributes (e.g: label, first name,…)
        directly in the SPARQL queries.
        If True, the predicates of the triplet whose values are instantiated will have their types checked
        against the allowed types listed in self.voc_attributes.
        Let's take an example:
        We are looking for a Thing whose attribute 'label' is "አዲስ አበባ".
        • Non strict mode will have its query restrained to elements satisfying
          the triplet '?Thing ?has_label "አዲስ አበባ".'.
          The predicate is left undetermined ("?has_label" is a variable).
        • In strict mode, we are strict about the types of predicates of the triplet.
          For the current class ('Thing'), those predicates will be listed in
          self.voc_attributes['has_label'] and combined in the SPARQL query.
          Here, for the example, we set 'has_label' allowed the RDF predicates 'rdfs:label' and u'wdt:P1813'.
          >>> print(self.voc_attributes['has_label'])
          >>> [u'rdfs:label', u'wdt:P1813']
          So in strict_mode, the query will be constrained to:
          "[…]{ ?Thing rdfs:label "አዲስ አበባ"  } UNION { ?Thing wdt:P1813 "አዲስ አበባ"  }.[…]
        """
        if check_type:
            # Restricting the query to elements of the current type
            # This will build a query with union of RDF checking the type (eg.Book):
            # [...] { ?Book a fabio:Book  } UNION [...] UNION { ?Book a schemaorg:Book  } .
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
        # (i.e stored in the instance variables beginning with "has_").
        for entity_name in entities_names:
            entity_value = normalize_str(self.__dict__.get(entity_name, None))
            # The instance has an instantiated value for a 'has_…' variable. This value will be the
            # object of an RDF triplet.
            if entity_value:
                try:
                    # For dates elements, the triplet literal must be formatted without quotes
                    obj = int(entity_value)
                except ValueError:
                    if entity_value[0:7] == u'http://':
                        obj = u'%s' % entity_value  # The entity is a raw URL
                    else:
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

    # --------------------------------------- #
    #       QUERIES LAUNCH AND PROCESS
    # --------------------------------------- #

    def query(self, strict_mode=False, check_type=True):
        """
        Launches the query of the current object to the specified endpoints, given the query options to constraints
        the types of the RDF triples predicates and retrieve the results.
        The queries options relies on the dictionaries contained in pyneql/utils/vocabulary.py.

        :param check_type: Boolean. Check the type of the object (e.g: Book, Person, Location,…)
        directly in the SPARQL queries.
        If True, the restriction of the object's type is done in the query.
        For instance, if the object is a Book, activating strict_mode will build queries where the object
        to find (?Book) is constrained by an union of RDF triples checking that ?Book is a Book:
        "[…] { ?Book a fabio:Book  } UNION […] UNION { ?Book a schemaorg:Book  } .

        :param strict_mode: Boolean. Check the type of the object's attributes (e.g: label, first name,…)
        directly in the SPARQL queries.
        If True, the predicates of the triplet whose values are instantiated will have their types checked
        against the allowed types listed in self.voc_attributes.
        Let's take an example:
        We are looking for a Thing whose attribute 'label' is "አዲስ አበባ".
        • Non strict mode will have its query restrained to elements satisfying
          the triplet '?Thing ?has_label "አዲስ አበባ".'.
          The predicate is left undetermined ("?has_label" is a variable).
        • In strict mode, we are strict about the types of predicates of the triplet.
          For the current class ('Thing'), those predicates will be listed in
          self.voc_attributes['has_label'] and combined in the SPARQL query.
          Here, for the example, we set 'has_label' allowed the RDF predicates 'rdfs:label' and u'wdt:P1813'.
          >>> print(self.voc_attributes['has_label'])
          >>> [u'rdfs:label', u'wdt:P1813']
          So in strict_mode, the query will be constrained to:
          "[…]{ ?Thing rdfs:label "አዲስ አበባ"  } UNION { ?Thing wdt:P1813 "አዲስ አበባ"  }.[…]
        """

        self._build_query(strict_mode, check_type)
        self.query_builder.add_endpoints(self.endpoints)
        self.query_builder.commit()
        self._process_results(check_type) # TODO: set another check_type

    # --- Queries processing: organising results --- #

    def _process_results(self, check_type=True):
        """Given the result of a SPARQL query to find a Thing, this creates a Thing with all the information
        gathered in the self.attributes dictionary.
        :param check_type: Boolean. Check the type of the object (e.g: Book, Person, Location,…)
        in the SPARQL queries results. All the results which does not have the proper type are excluded.
        If True, the restriction of the object's type is done in the query.
        For instance, if the object is a Book, activating strict_mode will build queries where the object
        to find (?Book) is constrained by an union of RDF triples checking that ?Book is a Book:
        "[…] { ?Book a fabio:Book  } UNION […] UNION { ?Book a schemaorg:Book  } .
        """

        if not check_type:
            logging.warning("Type checking is disabled for object %s" % str(self.__dict__))

        subj = self.args['subject'][1:]
        obj = self.args['object'][1:]
        pred = self.args['predicate'][1:]

        things = self._process_subject_url_results(pred, obj) \
            if self.__dict__.get('has_url', None) \
            else self._process_any_results(subj, pred, obj, check_type)

        # Wikimedia... (╯°□°）╯︵ ┻━┻ Accepting Wikimedia elements that correspond to an entity because
        # what we will have TODO is to filter them properly.
        unfiltered_wikimedia_things = [t for t in things.keys() if 'wd:' in t]
        for unfiltered_wikimedia_thing in unfiltered_wikimedia_things:
            things[unfiltered_wikimedia_thing][u'validated'] = 1

        for thing, thing_attribute in things.items():
            # Removing wrong things and adding the attributes of the correct thing
            if check_type and not thing_attribute.get(u'validated', False):
                things.pop(thing)
            else:
                # Identity
                self.attributes = merge_two_dicts_in_sets(
                    self.attributes,
                    {u'owl:sameAs': thing,
                     u'skos:exactMatch': thing
                     })

                self.attributes = merge_two_dicts_in_sets(self.attributes, thing_attribute)

    def _process_subject_url_results(self, pred, obj):
        """Return a dictionary of results for a query containing an URL as the subject of a triple."""
        things = {}
        result_dict_list = [{a: a1, b: b1} for (a, a1), (b, b1) in self.query_builder.results]
        result_dict_list = [{get_shortened_uri(item.get(pred)): item.get(obj)} for item in result_dict_list]
        if result_dict_list:
            things[self.__dict__.get('has_url')] = reduce(merge_two_dicts_in_sets, result_dict_list)
            # If we retrieved the thing using its URL,
            # we are sure the results correspond to the right thing.
            things[self.__dict__.get('has_url')][u'validated'] = 1
        return things

    def _process_any_results(self, subj, pred, obj, check_type=True):
        """ Return a dictionary of results for standard types of queries.
        TODO: Document better that part."""
        things = {}
        values_to_check = {
            v: e for e, v in self.__dict__.items()
            if e.startswith('has_') and self.__dict__.get(e, None)
        }

        # We need to check the type of the responses
        for result in self.query_builder.results:
            dict_results = {arg_name: get_shortened_uri(arg_value) for (arg_name, arg_value) in result}
            thing = dict_results.pop(subj, None)

            # Checking that it is the thing we are looking for
            if check_type and dict_results[obj] in values_to_check:
                value = dict_results[obj]
                properties = self.voc_attributes.get(values_to_check[value], False)
                if properties and dict_results[pred] in properties:
                    things[thing][u'validated'] = 1

            shortened_result = {dict_results[pred]: dict_results[obj]}
            things[thing] = merge_two_dicts_in_sets(things.get(thing, {}), shortened_result)

        return things

    # --------------------------------------- #
    #      Playing with the object
    # --------------------------------------- #

    def find_more_about(self, seen=set([])):
        """Deepens the search
        TODO: document"""

        same_entities_keys = [u'skos:exactMatch', u'owl:sameAs']

        # TODO: dirty, make that more legible
        same_entity_uris = set(itertools.chain.from_iterable([
            self.attributes.get(same_entities_key)
            if isinstance(self.attributes.get(same_entities_key), set)
            else set([self.attributes.get(same_entities_key)])
            for same_entities_key in same_entities_keys
        ]))

        if None in same_entity_uris:
            same_entity_uris.remove(None)

        to_see = same_entity_uris-seen
        if len(to_see) == 0:
            return

        for same_entity_uri in to_see:
            seen.add(same_entity_uri)
            same_entity = Thing(url=same_entity_uri)
            same_entity.add_query_endpoints(self.endpoints)
            same_entity.query()
            self.attributes = merge_two_dicts_in_sets(self.attributes, same_entity.attributes)
        self.find_more_about(seen)

    def get_attributes_with_keyword(self, keyword):
        """ For debuging purposes """
        return {k: v for k, v in self.attributes.items() if keyword in k}

    def get_external_ids(self):
        """
        Get the external ids of the Thing.
        """
        raise NotImplementedError('Subclasses must override get_external_ids()!')




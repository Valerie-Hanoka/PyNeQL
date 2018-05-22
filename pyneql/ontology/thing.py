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

from pyneql.utils.namespace import (
    get_shortened_uri,
    get_expended_uri
)
from pyneql.utils.utils import (
    QueryException,
    merge_two_dicts_in_sets,
    parse_literal_with_language
)

from pyneql.utils.utils import (
    normalize_str,
    is_listlike
)

from functools import reduce
from itertools import chain
import re

try:
    basestring
except NameError:
    basestring = str

class Thing(object):
    """
    A semantic representation of a Thing, retrieved from the Semantic Web.
    """

    setup_logging()

    # The regular expression matchin labels in the attribute dict.
    RE_LABEL = re.compile('[Ll]abel|[Nn]ame')

    # Query
    query_builder = None
    query_limit = None
    endpoints = None

    # Results
    attributes = None

    # Implementation convention
    # Elements which will be used to construct the query
    # for something more specific than a Thing
    # must begin with "has_".
    has_label = None
    has_url = None

    def __init__(
            self,
            query_language=Lang.DEFAULT,
            label=None,
            url=None,
            endpoints=None,  # SPARQL endpoints where the query should be sent
            limit=1500,
            class_name=u'Thing'
            ):
        """
        :param query_language: The language of the query
        :param label: The label which should be queried
        :param url: The URL/URI of the Semantic Web object we wish to query
        :param endpoints: The endoints where the query should be send
        :param limit: The limit puts an upper bound on the number of solutions returned by the query that will be stored.
        :param class_name: The name of the current class

        """

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
        self.query_limit = limit
        self.query_language = query_language

        # Adding Endpoints
        self.endpoints = set(endpoints) if endpoints else set([])

        # Initializing results set
        self.attributes = {}

        # Initializing literals by languages
        self.labels_by_languages = {}


    # --------------------------------------- #
    #           QUERIES PREPARATION
    # --------------------------------------- #

    # --- Queries parameters: endpoints --- #

    def add_query_endpoints(self, endpoints):
        """This function allows to add a list of endpoints to which the Thing queries will be sent.

        :param endpoints: A list of endpoints we wish to query for the construction of the current Thing.

        """
        for endpoint in endpoints:
            self.add_query_endpoint(endpoint)

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
        For instance, if the object is a Book, activating type checking will build queries where the object
        to find (?Book) is constrained by an union of RDF triples checking that ?Book is a Book:
        ``[…] { ?Book a fabio:Book  } UNION […] UNION { ?Book a schemaorg:Book  } .``

        :param strict_mode: Boolean. Check the type of the object's attributes (e.g: label, first name,…)
        directly in the SPARQL queries.
        If True, the predicates of the triplet whose values are instantiated will have their types checked
        against the allowed types listed in self.voc_attributes.
        Let's take an example:
        We are looking for a Thing whose *label* is "አዲስ አበባ".

        - Non strict mode will have its query restrained to elements satisfying
        the triplet ``?Thing ?has_label "አዲስ አበባ".``.
        The predicate is left undetermined (``?has_label`` is a variable).

        - In strict mode, we are strict about the types of predicates of the triplet.
        For the current class, those predicates will be listed in
        self.voc_attributes['has_label'] and combined in the SPARQL query.
        Here, for the example, we set 'has_label' allowed the RDF predicates 'rdfs:label' and u'wdt:P1813'.

        >>> print(self.voc_attributes['has_label'])
        >>> [u'rdfs:label', u'wdt:P1813']

        So in strict_mode, the query will be constrained to:
        
        ``[…]{ ?Thing rdfs:label "አዲስ አበባ"  } UNION { ?Thing wdt:P1813 "አዲስ አበባ"  }.[…]``

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
        """If the current object is already identified by an URL/URI or a list of URL/URIs,
         we can unambiguously query it/them.
        The URL(s) becomes the subject(s) of our RDF triple.
        """

        if is_listlike(self.has_url):

            # We have a list/set/tuple of URLs: the RDF triple will be:
            # `{ <URL1> ?pred ?obj  } UNION { <URL2> ?pred ?obj  } .`
            to_unite = set([])
            for url in self.has_url:
                to_unite.add(
                    RDFTriple(
                        subject=url,
                        predicate=self.args['predicate'],
                        object=self.args['object'],
                        language=self.query_language
                    )
                )
            
            self.query_builder.add_query_alternative_triples(to_unite)

        else:
            # We have a simple URL: the RDF triple will be:
            # `<URL> ?pred ?obj .`
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

        :param entities_names: the class variables beginning with 'has_' which have a value instantiated

        :param check_type: Boolean.
        Check the type of the object (e.g: Book, Person, Location,…)
        directly in the SPARQL queries.
        If True, the restriction of the object's type is done in the query.
        For instance, if the object is a Book, activating type checking will build queries where the object
        to find (?Book) is constrained by an union of RDF triples checking that ?Book is a Book:
        ``[…] { ?Book a fabio:Book  } UNION […] UNION { ?Book a schemaorg:Book  } .``

        :param strict_mode: Boolean.
        Check the type of the object's attributes (e.g: label, first name,…)
        directly in the SPARQL queries.
        If True, the predicates of the triplet whose values are instantiated will have their types checked
        against the allowed types listed in ``self.voc_attributes``.
        Let's take an example:
        We are looking for a Thing whose *label* is "አዲስ አበባ".

        - Non strict mode will have its query restrained to elements satisfying
        the triplet ``?Thing ?has_label "አዲስ አበባ".``.
        The predicate is left undetermined (``?has_label`` is a variable).

        - In strict mode, we are strict about the types of predicates of the triplet.
         For the current class, those predicates will be listed in
         ``self.voc_attributes['has_label']`` and combined in the SPARQL query.
         Here, for the example, we set 'has_label' allowed the RDF predicates 'rdfs:label' and u'wdt:P1813'.

         >>> print(self.voc_attributes['has_label'])
         >>> [u'rdfs:label', u'wdt:P1813']

         So in strict_mode, the query will be constrained to:

         ``[…]{ ?Thing rdfs:label "አዲስ አበባ"  } UNION { ?Thing wdt:P1813 "አዲስ አበባ"  }.[…]``
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
            entity_values = self.__dict__.get(entity_name, None)
            if is_listlike(entity_values):
                # TODO ici il faudrait créer des alternate triples
                self.create_triples_for_multiple_element(entity_name, entity_values)

            else:
                entity_value = normalize_str(entity_values)
                self.create_triples_for_single_element(entity_name, entity_value, strict_mode)

        # Fetching everything about that Thing
        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=self.args['predicate'],
                object=self.args['object'],
                language=self.query_language
            )
        )

    def format_value_for_RDF_compliance(self, value, default_value):
        """
        An element of a RDF triple must have a certain form depending on it type:

        - Integers are given as is

        - URL/URIs must be enclosed in angle brackets.

        - Normal strings must be enclosed in quotation marks

        - If the value is empty or None, then the default value is prefixed with a question mark
          and becomes a variable.

        :param value: The value to be passed to a subject or object RDF slot.
        :param default_value: The name of the variable in case the value is empty.
        :return: A formatted value that will be a legal subject or object of an RDF triple.
        """

        if value:
            try:
                # For dates elements, the triplet literal must be formatted without quotes
                formatted_value = int(value)
            except ValueError:
                if value[0:7] == u'http://':
                    formatted_value = u'%s' % value  # The entity is a raw URL
                else:
                    formatted_value = u'"%s"' % value
        else:
            # If no value was specified, the object will be a variable in the SPARQL query
            formatted_value = u'?%s' % default_value

        return formatted_value

    def create_triples_for_multiple_element(self, entity_name, entity_values):
        """
        If the variable 'has_…' (entity_name) is a list of values instead of a single value,
        we create an alternate triple.
        N.B.: If strict mode is enabled for the query, it will be disabled
        for this particular triples union because this would increase the size of the query too much.

        :Example:

        >>> has_author = ["http://www.example.org/X", "http://www.example.org/Y"]
        Will give the query triple:
        `{ ?Book has_author <http://www.example.org/X>  } UNION { ?Book has_author <http://www.example.org/Y>  }.`

        :param entity_name: name of the 'has_…' attribute
        :param entity_values: values of the 'has_…' attribute
        :return:
        """
        logging.debug("Strict mode is disabled for %s because it contains multiple values." % entity_name)

        to_unite = set([])
        for entity_value in entity_values:
            to_unite.add(
                RDFTriple(
                    subject=self.args['subject'],
                    predicate=u'?%s' % entity_name,
                    object=self.format_value_for_RDF_compliance(entity_value, u"%s_obj" % entity_name),
                    language=self.query_language
                )
            )
        self.query_builder.add_query_alternative_triples(to_unite)



    def create_triples_for_single_element(self, entity_name, entity_value,  strict_mode):
        """
        If the variable 'has_…' (entity_name) is a single values instead of a list of value,
        we create a standard query triple.

        :param entity_name: name of the 'has_…' attribute
        :param entity_value: values of the 'has_…' attribute
        :param strict_mode: is strict_mode (check RDF type) is enabled
        :return:
        """

        # The instance has an instantiated value for a 'has_…' variable. This value will be the
        # object of an RDF triplet.
        obj = self.format_value_for_RDF_compliance(entity_value, u"%s_obj" % entity_name)
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

    # --------------------------------------- #
    #       QUERIES LAUNCH AND PROCESS
    # --------------------------------------- #

    def query(self, strict_mode=False, check_type=True, limit=1500):
        """
        Launches the query of the current object to the specified endpoints, given the query options to constraints
        the types of the RDF triples predicates and retrieve the results.
        The queries options relies on the dictionaries contained in pyneql/utils/vocabulary.py.

        :param check_type: Boolean.

        Check the type of the object (e.g: Book, Person, Location,…) directly in the SPARQL queries.
        If True, the restriction of the object's type is done in the query.
        For instance, if the object is a Book, activating type checking will build queries where the object
        to find (?Book) is constrained by an union of RDF triples checking that ?Book is a Book:
        ``[…] { ?Book a fabio:Book  } UNION […] UNION { ?Book a schemaorg:Book  } .``

        :param strict_mode: Boolean.

        Check the type of the object's attributes (e.g: label, first name,…) directly in the SPARQL queries.
        If True, the predicates of the triplet whose values are instantiated will have their types checked
        against the allowed types listed in self.voc_attributes.


        :Example:

        We are looking for a Thing whose *label* is "አዲስ አበባ".

        - Non strict mode will have its query restrained to elements satisfying
        the triplet ``?Thing ?has_label "አዲስ አበባ".``.
        The predicate is left undetermined (``?has_label`` is a variable).

        - In strict mode, we are strict about the types of predicates of the triplet.
        For the current class, those predicates will be listed in
        ``self.voc_attributes['has_label']`` and combined in the SPARQL query.
        Here, for the example, we set 'has_label' allowed the RDF predicates 'rdfs:label' and u'wdt:P1813'.

        >>> print(self.voc_attributes['has_label'])
        >>> [u'rdfs:label', u'wdt:P1813']

        So in strict_mode, the query will be constrained to:

        ``[…]{ ?Thing rdfs:label "አዲስ አበባ"  } UNION { ?Thing wdt:P1813 "አዲስ አበባ"  }.[…]``
        """

        self.query_builder.set_limit(self.query_limit)
        self._build_query(strict_mode=strict_mode, check_type=check_type)
        self.query_builder.add_endpoints(self.endpoints)
        self.query_builder.commit()
        self._process_results(check_type)  # TODO: set another check_type

    # --- Queries processing: organising results --- #

    def _process_results(self, check_type=True):
        """Given the result of a SPARQL query to find a Thing, this creates a Thing with all the information
        gathered in the self.attributes dictionary.
        :param check_type: Boolean. Check the type of the object (e.g: Book, Person, Location,…)
        in the SPARQL queries results. All the results which does not have the proper type are excluded.
        If True, the restriction of the object's type is done in the query.

        :Example:

        If the object is a Book, activating type checking will build queries where the object
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

        things_items = list(things.items())
        for thing, thing_attribute in things_items:
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

        # Fetching all the literals and organizing them by language
        self._organise_labels_by_language()


    def _process_subject_url_results(self, pred, obj):
        """Return a dictionary of results for a query containing an URL as the subject of a triple."""
        things = {}
        result_dict_list = [{a: a1, b: b1} for (a, a1), (b, b1) in self.query_builder.results]
        result_dict_list = [{get_shortened_uri(item.get(pred)): item.get(obj)} for item in result_dict_list]
        if result_dict_list:
            urls = self.__dict__.get('has_url') \
                if is_listlike(self.__dict__.get('has_url')) \
                else [self.__dict__.get('has_url')]

            for url in urls:
                things[url] = reduce(merge_two_dicts_in_sets, result_dict_list)
                # If we retrieved the thing using its URL,
                # we are sure the results correspond to the right thing.
                things[url][u'validated'] = 1
        return things

    def _process_any_results(self, subj, pred, obj, check_type=True):
        """ Return a dictionary of results for standard types of queries.
        TODO: Document better that part."""

        # The dict 'thing' will keep track of all the semantic web objects
        # that are returned by the query
        things = {}

        # We need to check only the object's instantiated "has_..." values
        values_to_check = {}
        for element, value in self.__dict__.items():
            if element.startswith('has_') and self.__dict__.get(element, None):
                if is_listlike(value):
                    for v in value:
                        values_to_check[v] = element
                else:
                    values_to_check[value] = element

        # If check_type is set to True, we need to check the type of the responses
        for result in self.query_builder.results:
            dict_results = {arg_name: get_shortened_uri(arg_value) for (arg_name, arg_value) in result}
            thing = dict_results.pop(subj, None)

            # Checking that the result is of the right type
            if check_type and dict_results[obj] in self.rdf_types:
                things[thing] = {u'validated': 1}

            shortened_result = {dict_results[pred]: dict_results[obj]}
            things[thing] = merge_two_dicts_in_sets(things.get(thing, {}), shortened_result)

        return things

    # --------------------------------------- #
    #      Playing with the object
    # --------------------------------------- #

    def find_more_about(self):
        """Deepens the search"""
        self._recursively_find_more_about(set([]))
        self._organise_labels_by_language()

    def _recursively_find_more_about(self, seen=set([])):
        """TODO: document"""

        same_entities_keys = [u'skos:exactMatch', u'owl:sameAs']

        # TODO: dirty, make that more legible
        same_entity_uris = set(chain.from_iterable([
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
        self._recursively_find_more_about(seen)

    def get_uris(self):
        """ Gets the URIs of the current object. """
        identity_predicates = [u'owl:sameAs', u'skos:exactMatch']
        urls_sets = [self.attributes.get(pred) for pred in identity_predicates]
        urls = set([get_expended_uri(u) for u in chain.from_iterable(urls_sets)])
        return [url for url in urls if url]

    def get_attributes_with_keyword(self, keyword):
        """ Returns the attributes whose predicates contains a keyword.

        :Example:

        >>> my_thing.get_attributes_with_keyword('rdfs:')
        will return all the attributes whose values' keys contains rdfs:
        rdfs:label, rdf:type, subClassOf, rdfs:seeAlso ...
        """

        return {k: v for k, v in self.attributes.items() if re.search(keyword, k)}

    def _organise_labels_by_language(self):
        """
        Get all the labels in the results and populates self.literals_by_language
        with them.
        :return: None
        """
        for labels_with_languages in self.get_attributes_with_keyword(self.RE_LABEL).values():
            if isinstance(labels_with_languages, basestring):
                labels_with_languages = [labels_with_languages]
            for label_with_language in labels_with_languages:
                label, language = parse_literal_with_language(label_with_language)
                language = language if language else self.query_language.value
                if language:
                    stored_labels = self.labels_by_languages.get(language, [])
                    stored_labels.append(label)
                    self.labels_by_languages[language] = stored_labels

    def get_external_ids(self):
        """
        Get the external ids of the Thing.
        """
        raise NotImplementedError('Subclasses must override get_external_ids()!')




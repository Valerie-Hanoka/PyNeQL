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
from pyneql.utils.vocabulary import (
    rdf_types,
    attributes
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

    def __init__(
            self,
            query_language=Lang.DEFAULT,
            endpoints=None,  # SPARQL endpoints where the query should be sent
            class_name=u'Thing'
            ):

        if not isinstance(query_language, Lang):
            raise QueryException("The language of the query must be of type enum.LanguagesIso6391.")

        self.rdf_types = rdf_types[class_name]
        self.thing_attributes = attributes[class_name]

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

    def _build_query(self):
        raise NotImplementedError

    def query(self):

        self._build_query()
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
                properties = self.thing_attributes.get(values_to_check[value], False)
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
        ark
        viaf
        d - nb.info  # dnb (Deutschen Nationalbibliothek)
        wikidata.org
        idref
        """
        ids = {}
        external_ids = self.attributes.get(u'owl:sameAs').union(self.attributes.get(u'skos:exactMatch'))
        for external_id in external_ids:
            if u'ark' in external_id:
                ids[u'ark'] = external_id
            elif u'viaf' in external_id:
                ids[u'viaf'] = external_id
            elif u'd-nb.info' in external_id:
                ids[u'Deutschen_Nationalbibliothek'] = external_id
            elif u'wikidata.org' in external_id:
                ids[u'wikidata'] = external_id
            elif u'idref' in external_id:
                ids[u'idref'] = external_id

        return ids

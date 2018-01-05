#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
personquerybuilder is part of the project PyNeQL
Author: Valérie Hanoka

"""

from pyneql.ontology.thing import Thing
from pyneql.log.loggingsetup import (
    setup_logging,
)


from pyneql.query.rdftriple import RDFTriple
from pyneql.utils.enum import (
    LanguagesIso6391 as Lang,
)

from pyneql.utils.endpoints import Endpoint
from pyneql.utils.utils import (
    QueryException,
    contains_a_date,
    merge_two_dicts_in_sets
)
from datetime import datetime


class Person(Thing):
    """
    A semantic representation of a person, retrieved from the Semantic Web.
    """

    setup_logging()

    # Elements which will be used to construct the query for a Person
    has_full_name = None
    has_last_name = None
    has_first_name = None
    has_birth_year = None
    has_death_year = None

    def __init__(self,
                 full_name=None, last_name=None, first_name=None,
                 birth_year=None, death_year=None,
                 query_language=Lang.DEFAULT,
                 endpoints=None,  # SPARQL endpoints where the query should be sent
                 class_name=u'Person'
                 ):

        if not (full_name or ((first_name or birth_year or death_year) and last_name)):
            raise QueryException("There is not enough information provided to find this person."
                                 " Provide full name information.")

        self.has_full_name = full_name
        self.has_last_name = last_name
        self.has_first_name = first_name
        self.has_birth_year = birth_year
        self.has_death_year = death_year
        super(Person, self).__init__(query_language=query_language, endpoints=endpoints, class_name=class_name)

    def _build_query(self):

        # Restricting the query to only Person elements
        # For all Endpoints except Wikidata, it is simple and efficient to
        # keep only entities that are of type foaf:Person.
        # Wikidata does not respond well to that triple, so for this endpoint only,
        # we use predicate wdt:P31 and value wd:Q5 (human being)."
        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=u'wdt:P31',
                object=u'wd:Q5',
                keep_only_endpoints=[Endpoint.wikidata],
                language=self.query_language
            )
        )

        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=u'a',
                object=u'foaf:Person',
                excluded_endpoints=[Endpoint.wikidata],
                language=self.query_language
            )
        )

        # Adding query delimiters
        entities_names = [e for e in self.__dict__.keys() if e.startswith('has_') and self.__dict__.get(e, False)]
        for entity_name in entities_names:
            tmp = self.__dict__.get(entity_name, None)
            if tmp:
                try:
                    tmp = int(tmp)
                    obj = tmp
                except:
                    obj = u'"%s"' % tmp
            else:
                obj = u'?%s' % entity_name
            pred = u'?%s' % entity_name
            self.query_builder.add_query_triple(
                RDFTriple(
                    subject=self.args['subject'],
                    predicate=pred,
                    object=obj,
                    language=self.query_language
                )
            )

        # Fetching everything about that person
        self.query_builder.add_query_triple(
            RDFTriple(
                subject=self.args['subject'],
                predicate=self.args['predicate'],
                object=self.args['object'],
                language=self.query_language
            )
        )

    def _get_life_info(self, life_event='birth'):
        """For a given information type (i.e death, birth), this function
        returns all information that is available in the linked data about the
        life event of the person (e.g: date and/or place).
        :param life_event: An event of the life of a person (e.g.: birth, death)
        :return: a dict of information concerning the given life event
        """
        biography_info = {}
        already_contains_birth_date = False # True if and only if we already have a full date
        for k, v in self.attributes.items():
            if life_event in k.lower():
                infos = v if isinstance(v, set) else set([v])
                for info in infos:
                        if contains_a_date(info):
                            if already_contains_birth_date:
                                continue
                            try:
                                split = info.count('-')
                                if split == 2:
                                    # Full birth date
                                    # Keeping only this date information, as it is the
                                    # most informative
                                    biography_info['date'] = datetime.strptime(info, '%Y-%m-%d')
                                    already_contains_birth_date = 1
                                    continue
                                else:
                                    # Partial birth date
                                    if split == 1:
                                        # Only year and month
                                        info = datetime.strptime(info, '%Y-%m')
                                    else:
                                        # Only year
                                        info = datetime.strptime(info, '%Y')

                                    biography_info = merge_two_dicts_in_sets(
                                        biography_info,
                                        {'date': info})
                            except ValueError:
                                # No available date info to parse
                                continue
                        else:
                            biography_info = merge_two_dicts_in_sets(
                                biography_info,
                                {'place': info})
        return biography_info

    def get_death_info(self):
        """This function returns all information that is available in the linked data
         about the death of the person (e.g: date and/or place).
        :return: a dict of information concerning the death of the person
        """
        return self._get_life_info('death')

    def get_birth_info(self):
        """This function returns all information that is available in the linked data
         about the birth of the person (e.g: date and/or place).
        :return: a dict of information concerning the birth of the person
        """
        return self._get_life_info('birth')

    def get_gender(self):
        """ Get the gender of the person.
        We assume that there is only one gender available for a person in the retrieved data.
        :return:
          - ♀ if the person is labelled as a woman
          - ♂ if the person is labelled as a man
          - ∅ if the gender information is unavailable."""
        gender = self.attributes.get(u'foaf:gender').pop()
        if gender is u'female':
            return u'♀'
        elif gender is u'male':
            return u'♂'
        else:
            return u'∅'



    def get_normalized_name(self):
        """

        :return:
        """
        pass
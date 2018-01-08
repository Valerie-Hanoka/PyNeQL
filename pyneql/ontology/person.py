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

from dateutil.parser import parse as parsedate
from itertools import chain

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

        # Adding query delimiters, that are the parameters given for query
        # (i.e stored in the instance variables begining with "has_").
        # For instance, Person(full_name="Jemaine Clement") will have its query
        # restrained to elements satisfying the triplet '?Person ?has_full_name "Jemaine Clement."'.
        entities_names = [e for e in self.__dict__.keys() if e.startswith('has_') and self.__dict__.get(e, False)]
        for entity_name in entities_names:
            tmp = self.__dict__.get(entity_name, None)
            if tmp:
                try:
                    # For dates elements, the triplet literal must be formatted without quotes
                    obj = int(tmp)
                except ValueError:
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
                    if info.count('-') > 4:
                        continue
                    if contains_a_date(info):
                        if already_contains_birth_date:
                            continue
                        try:
                            biography_info['date'] = parsedate(info)
                            already_contains_birth_date = 1
                        except ValueError:
                            # No available date info to parse
                            continue
                    elif 'place' in k:
                        biography_info = merge_two_dicts_in_sets(
                            biography_info,
                            {'place': info})
                    elif 'name' in k:
                        biography_info = merge_two_dicts_in_sets(
                            biography_info,
                            {'name': info})
                    elif 'cause' in k or 'manner' in k:
                        biography_info = merge_two_dicts_in_sets(
                            biography_info,
                            {'cause/manner': info})

                    else:
                        biography_info = merge_two_dicts_in_sets(
                            biography_info,
                            {'other': info})


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

        # Wikidata

        for info_key, info in self.attributes.iteritems():
            if 'gender' in info_key.lower():
                genders = {
                    u'female': u'F',
                    u'Q6581072': u'F',
                    u'male': u'M',
                    u'Q6581097': u'M',
                    u'Q1052281': u'MtF',
                    u'Q2449503': u'FtM',
                    u'Q1097630': u'intersex',
                }
                gender = next(iter(info)) if isinstance(info, set) else info
                return genders.get(gender[gender.find(':') + 1:], u'unknown')
        return u'unknown'

    def get_names(self):
        """This function returns all information that is available in the linked data
         about the name of the person (e.g: birth name, family name, name in the native language,...).
        :return: a dict of information concerning the names of the person.
        """

        # Idiomatic elements
        # A dirty way to get all the names that does not contain 'name' in their names
        idiomatic_name_keys = {
            v for v in chain.from_iterable([n for k, n in self.thing_attributes.items() if 'name' in k])
            if 'name' not in v
        }

        unfiltered_names = {
            k: v for k, v in self.attributes.iteritems()
            if 'name' in k or k in idiomatic_name_keys
        }
        names = {}

        for name_type, name in unfiltered_names.items():
            if isinstance(name, set):
                filtered = filter(lambda x: x.count('-') < 5, name)
                if filtered:
                    names[name_type] = filtered if len(filtered)>1 else filtered.pop()
            else:
                if name.count('-') < 5:

                    names[name_type] = name
        return names
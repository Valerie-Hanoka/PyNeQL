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

from pyneql.utils.enum import (
    LanguagesIso6391 as Lang,
)

from pyneql.utils.utils import (
    QueryException,
    contains_a_date,
    merge_two_dicts_in_sets,
    normalize_str,
    parse_literal_with_language
)

from dateutil.parser import parse as parsedate
from itertools import chain

import six


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

    has_url = None

    def __init__(self,
                 full_name=None, last_name=None, first_name=None,
                 url=None,
                 # birth_year=None, death_year=None,
                 query_language=Lang.DEFAULT,
                 endpoints=None,  # SPARQL endpoints where the query should be sent
                 class_name=u'Person'
                 ):

        if not (full_name or (first_name and last_name) or url):  # or birth_year or death_year
            raise QueryException("There is not enough information provided to find this person."
                                 " Provide full name information.")

        self.has_full_name = normalize_str(full_name) if full_name else None
        self.has_last_name = normalize_str(last_name) if last_name else None
        self.has_first_name = normalize_str(first_name) if first_name else None

        # self.has_birth_year = birth_year
        # self.has_death_year = death_year
        super(Person, self).__init__(
            url=url,
            query_language=query_language,
            endpoints=endpoints,
            class_name=class_name
        )

    def _get_life_info(self, life_event):
        """For a given information type (i.e death, birth), this function
        returns all information that is available in the linked data about the
        life event of the person (e.g: date and/or place).

        :param life_event: An event of the life of a person (e.g.: birth, death)
        :return: a dict of information concerning the given life event
        """
        biography_info = {}
        already_contains_birth_date = False  # True if and only if we already have a full date
        for k, v in self.attributes.items():
            k = k.lower()
            if life_event in k:
                all_info = v if isinstance(v, set) else {v}
                for info in all_info:
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
        """This function returns the gender of the person.
        We assume that there is only one gender available for a person in the retrieved data.

        :return:

        - 'F' if the person is labelled as a woman
        - 'M' if the person is labelled as a man
        - 'MtF', 'FtM', 'intersex' or 'queer' if the person is transgender or genderqueer.
        - 'unknown' if the gender information is unavailable."""

        genders = {
            u'female': u'F',
            u'Q6581072': u'F',
            u'male': u'M',
            u'Q6581097': u'M',
            u'Q1052281': u'MtF',
            u'Q2449503': u'FtM',
            u'Q1097630': u'intersex',
            u'genderqueer': u'queer'
        }

        retrieved_genders = [
            parse_literal_with_language(g)
            for g
            in self.get_attributes_with_keyword('gender').values()
        ]

        for gender, lang in retrieved_genders:

            # We take the first declared gender in the iterator (others -if any- are ignored)
            g = genders.get(gender[gender.find(':') + 1:], None)
            if g is not None:
                return g
        return u'unknown'

    def get_names(self):
        """This function returns all information that is available in the linked data
        about the name of the person (e.g: birth name, family name, name in the native language,...).

        :return: a dict of information concerning the names of the person.
        """

        # Idiomatic elements
        # A dirty way to get all the names that does not contain 'name' in their names
        idiomatic_name_keys = {
            v for v in chain.from_iterable([n for k, n in self.voc_attributes.items() if 'name' in k])
            if 'name' not in v
        }

        unfiltered_names = {
            k: v for k, v in six.iteritems(self.attributes)
            if 'name' in k or k in idiomatic_name_keys
        }
        names = {}

        for name_type, name in unfiltered_names.items():
            if isinstance(name, set):
                filtered = [n for n in name if n.count('-') < 5]
                if filtered:
                    names[name_type] = filtered if len(filtered) > 1 else filtered.pop()
            else:
                if name.count('-') < 5:

                    names[name_type] = name
        return names

    def get_external_ids(self):
        """This function returns a curated list of external ids of the Person.

        :return: a dict of Person ids such as VIAF, Wikidata, IDREF, ARK,...
        """
        ids = {}

        same_as = self.attributes.get(u'owl:sameAs')
        same_as = same_as if isinstance(same_as, set) else {same_as}

        exact_match = self.attributes.get(u'skos:exactMatch')
        exact_match = exact_match if isinstance(exact_match, set) else {exact_match}

        external_ids = same_as.union(exact_match)

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

    # def get_works(self):
    #     """This function returns the works of a person.
    #     Not implemented yet.
    #     """
    #     # TODO
    #     # wdt:P1455
    #     # http://purl.org/dc/terms/contributor
    #     raise NotImplementedError

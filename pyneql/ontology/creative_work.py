#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
creative_work.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from pyneql.ontology.thing import Thing
from pyneql.ontology.person import Person

from pyneql.log.loggingsetup import (
    setup_logging,
)

from pyneql.utils.enum import (
    LanguagesIso6391 as Lang,
)

from pyneql.utils.utils import (
    QueryException,
)

class CreativeWork(Thing):
    """
    A semantic representation of the most generic kind of creative work,
    including books, movies, photographs, software programs, etc.
    """

    setup_logging()

    # Elements which will be used to construct the query for a Person
    has_title = None
    has_author = None
    has_date = None
    has_url = None

    def __init__(self,
                 title=None,
                 author=None,
                 author_is_organisation=False,
                 date=None,
                 url=None,
                 query_language=Lang.DEFAULT,
                 endpoints=None,  # SPARQL endpoints where the query should be sent
                 class_name=u'CreativeWork'
                 ):

        # The author may be a Person or an Organization
        if author:
            if isinstance(author, Person) or isinstance(author, Thing):     # TODO: Implement organisation
                self.has_author = author.get_uris()
                if not self.has_author:
                    raise QueryException("The given author is invalid (no URI found).")
            else:
                if author_is_organisation:
                    self.has_author = self.find_author_organisation(author, query_language)
                else:
                    self.has_author = self.find_author_person(author, query_language)

        self.has_title = title
        self.has_date = date
        self.has_url = url

        super(CreativeWork, self).__init__(
            url=url,
            query_language=query_language,
            endpoints=endpoints,
            class_name=class_name
        )


    def find_author_person(self, author, query_language, strict_mode=True, check_type=True):
        """ Find a Person corresponding to an author name.
        :param author: Full name of the author
        :param query_language: The language declared in the Book query
        :return:
        """

        author = Person(full_name=author, query_language=query_language)
        author.query(strict_mode=strict_mode, check_type=check_type)
        if not author.attributes:
            raise QueryException("The author could be found on the Semantic Web.")
        return author.get_uris()

    def find_author_organisation(self, author, query_language, strict_mode=True, check_type=True):
        """ Find an Organisation corresponding to an author name.
        :param author: Full name of the Organisation
        :param query_language: The language declared in the Book query
        :return:
        """
        # raise NotImplementedError("The Class 'Organisation' is not implemented yet !")

        author = Thing(label=author, query_language=query_language)
        author.query(strict_mode=strict_mode, check_type=check_type)
        if not author.attributes:
            raise QueryException("The authoring organisation could be found on the Semantic Web.")
        return author.get_uris()

#    def query(self, strict_mode=False, check_type=False):
#        super(CreativeWork, self).query(strict_mode=strict_mode, check_type=check_type)


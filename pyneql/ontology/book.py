#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
book is part of the project PyNeQL
Author: Valérie Hanoka

"""

from pyneql.ontology.creative_work import CreativeWork
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


class Book(CreativeWork):
    """
    A semantic representation of a book.
    """

    setup_logging()

    # Elements which will be used to construct the query for a Person
    has_publisher = None
    has_gallica_url = None

    def __init__(self,
                 title=None,
                 author=None,
                 publisher=None,
                 publication_date=None,
                 gallica_url=None,
                 url=None,
                 query_language=Lang.DEFAULT,
                 endpoints=None,  # SPARQL endpoints where the query should be sent
                 class_name=u'Book'
                 ):

        if not (url or gallica_url or ((author or publication_date or publisher) and title)):
            raise QueryException("There is not enough information provided to find this creative work."
                                 " Provide more information.")

        self.has_publisher = publisher
        self.has_gallica_url = gallica_url
        self.has_url = url


        super(Book, self).__init__(
            title=title,
            author=author,
            date=publication_date,
            url=url,
            query_language=query_language,
            endpoints=endpoints,
            class_name=class_name
        )

    def query(self, strict_mode=False, check_type=False):
        super(Book, self).query(strict_mode=strict_mode, check_type=check_type)


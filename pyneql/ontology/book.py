#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
book is part of the project PyNeQL
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

class Book(Thing):
    """
    A semantic representation of a physical or virtual object made by humans.
    """

    setup_logging()

    # Elements which will be used to construct the query for a Person
    has_title = None
    has_author = None
    has_publisher = None
    has_publication_date = None
    has_url = None

    def __init__(self,
                 title=None,
                 author=None,
                 publisher=None,
                 publication_date=None,
                 url=None,
                 query_language=Lang.DEFAULT,
                 endpoints=None,  # SPARQL endpoints where the query should be sent
                 class_name=u'Book'
                 ):

        if not (url or ((author or publication_date or publisher) and title)):
            raise QueryException("There is not enough information provided to find this creative work."
                                 " Provide more information.")

        self.has_title = title
        self.has_author = author
        self.has_publisher = publisher
        self.has_publication_date = publication_date
        self.has_url = url

        super(Book, self).__init__(
            url=url,
            query_language=query_language,
            endpoints=endpoints,
            class_name=class_name
        )



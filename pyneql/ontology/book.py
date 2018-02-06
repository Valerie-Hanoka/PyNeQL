#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
book is part of the project PyNeQL
Author: Valérie Hanoka

"""

from pyneql.ontology.thing import Thing
from pyneql.ontology.person import Person

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
    TODO
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
                 gallica_url=None,
                 url=None,
                 query_language=Lang.DEFAULT,
                 endpoints=None,  # SPARQL endpoints where the query should be sent
                 class_name=u'Book'
                 ):

        if not (url or gallica_url or ((author or publication_date or publisher) and title)):
            raise QueryException("There is not enough information provided to find this creative work."
                                 " Provide more information.")

        self.has_title = title
        self.has_publisher = publisher
        self.has_publication_date = publication_date
        self.has_gallica_url = gallica_url
        self.has_url = url

        super(Book, self).__init__(
            url=url,
            query_language=query_language,
            endpoints=endpoints,
            class_name=class_name
        )

        # Finding the author, if specified
        #if author:
        #    RDFTriple(subject=)
        # TODO

    def find_author(self, author_name, query_language):
        """Find a person corresponding to an author name.
        """

        author = Person(full_name=author_name, query_language=query_language)
        author.query()
        ids = author.get_external_ids()

        return ids.get('ark',
                       ids.get('viaf', author_name))




#PREFIX dc: <http://purl.org/dc/terms/&gt;
#PREFIX bibo: <http://purl.org/ontology/bibo/&gt;
#PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#&gt;
#SELECT DISTINCT ?book ?title ?subject ?label ?property ?value
#WHERE {
#?book a bibo:Book .
#?book dc:title ?title.
#?book bibo:isbn <urn:isbn:019857519x>.
#?book dc:subject ?subject.
#http://purl.org/dc/terms/
#OPTIONAL { ?subject rdfs:label ?label }
#OPTIONAL { ?subject ?property ?value }
#} GROUP BY ?book order by ?subject LIMIT 50
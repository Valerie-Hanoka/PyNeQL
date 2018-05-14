#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka
"""

# Debug:

from pyneql.ontology.thing import Thing
from pyneql.utils.enum import LanguagesIso6391 as Lang
from pyneql.utils.endpoints import Endpoint
import dataset

from pyneql.query.rdftriple import RDFTriple
from pyneql.query.querybuilder import GenericSPARQLQuery
from pyneql.utils.namespace import NameSpace
from fuzzywuzzy import fuzz

import pprint, ipdb

from pyneql.ontology.person import Person


from pyneql.utils.utils import pretty_print_utf8

from pyneql.ontology.person import Person
from pyneql.ontology.creative_work import CreativeWork
from pyneql.ontology.book import Book
from pyneql.utils.endpoints import Endpoint
from pyneql.utils.enum import LanguagesIso6391 as Lang


# Creating the person using its first and last names.
# Default language is English.
bell_hooks = Person(first_name="bell", last_name="hooks")

# In order to query the new person in the Semantic Web, we should
# add at least one endpoint. Here, we add them all:
endpoints = [e for e in Endpoint]
bell_hooks.add_query_endpoints(endpoints)

# Sending the query
bell_hooks.query()

ipdb.set_trace()

lemmas = ["chair", "law", "right", "beaver"]
things = []
for lemma in lemmas:
    thing = Thing(
        label=lemma,
        limit=100,
        endpoints=[Endpoint.wikidata, Endpoint.dbpedia, Endpoint.dbpedia_fr],
        query_language=Lang.English
    )

    thing.query(check_type=False, strict_mode=False)
    thing.find_more_about()
    things.append(thing)

book = Book(
    author='Virginia Woolf',
    title="A Room of One's Own",
    endpoints=[e for e in Endpoint])
book.query()

#for e in Endpoint:
#    assert fuzz.token_sort_ratio(expected_queries[e], thing.query_builder.queries[e]) == 100

ipdb.set_trace()


db = dataset.connect(u'sqlite:////Users/hanoka/obvil/TEIExplorer/useAndReuse.db')


#persons(db, endpoints)
#books(db, endpoints)



def books(db, endpoints):
    book_table = db['identifier']
    for row in book_table:
        print(row)
        if row.get('type') == u'url' and row.get('idno'):
            book =  Book(gallica_url=row.get('idno'))
            book.add_query_endpoints(endpoints)
            book.query(check_type=False)
            book.find_more_about()
            pprint.pprint(book.attributes)

#books(db, endpoints)


def persons(db, endpoints):
    person_table = db['person']
    people = {}
    for row in person_table:
        (first_name, last_name) = row.get('first_name_or_initials').strip(), row.get('last_name').strip()
        full_name = u'%s %s' % (first_name, last_name)
        try:
            birth = int(row.get('birth', "None") or "None")
        except ValueError:
            birth = None
        try:
            death = int(row.get('death', "None")or "None")
        except ValueError:
            death = None

        fingerprint = u"%s %s %s" % (
            full_name.strip(),
            birth,
            death
        )
        print("%s  ---  %s" % (row.get('fingerprint'), fingerprint, ))
        if first_name and last_name:
            person = Person(
                full_name=full_name.strip(),
                query_language=Lang.French
            )
            person.add_query_endpoints(endpoints)

            person.query()
            if person.attributes:
                people[fingerprint] = {'person': person}

            else:
                people[fingerprint] = {'person': None}
            import ipdb; ipdb.set_trace()
            people[fingerprint]['old_fingerprint'] = row.get('fingerprint')
    import ipdb; ipdb.set_trace()


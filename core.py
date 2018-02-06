#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka
"""

# Debug:

from pyneql.ontology.book import Book
from pyneql.utils.enum import LanguagesIso6391 as Lang
from pyneql.utils.endpoints import Endpoint
import dataset

from pyneql.query.rdftriple import RDFTriple
from pyneql.query.querybuilder import GenericSPARQLQuery
from pyneql.utils.namespace import NameSpace
from fuzzywuzzy import fuzz

from pyneql.ontology.thing import Thing
from pyneql.ontology.person import Person
import pprint, ipdb


endpoints = [Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf]
db = dataset.connect(u'sqlite:////Users/hanoka/obvil/TEIExplorer/useAndReuse.db')

thing = Thing(label=u"Л’Иль-д’Абоe", query_language=Lang.Russian)
thing.add_query_endpoint(Endpoint.dbpedia)
thing.query_builder.set_limit(666)
thing.query(strict_mode=False)

expected = {
    'endpoints': set([Endpoint.dbpedia]),
    'has_label': u"Л’Иль-д’Абоe",
    'query_language': Lang.Russian,
}
print thing.endpoints == expected.get('endpoints')
print thing.has_label == expected.get('has_label')
print thing.query_language == expected.get('query_language')
print thing.attributes.get(u'owl:sameAs') == u'wd:Q36494'  # https://www.wikidata.org/wiki/Q36494

import ipdb; ipdb.set_trace()

#thing = Person(full_name="Marguerite Duras", query_language=Lang.French)
#thing = Book(gallica_url=u"http://gallica.bnf.fr/ark:/12148/bpt6k6258559w")

thing = Book(
    #title=u"Les Misérables",
    #author=u"Charles Baudelaire",
    gallica_url=u"http://gallica.bnf.fr/ark:/12148/bpt6k6258559w",
    query_language=Lang.French,
    endpoints=endpoints
)


thing.query(strict_mode=False, check_type=False)
#thing.deepen_search()
pprint.pprint(thing.attributes)
import ipdb; ipdb.set_trace()




#persons(db, endpoints)
#books(db, endpoints)



def books(db, endpoints):
    book_table = db['identifier']
    for row in book_table:
        print "_____________________________"
        print(row)
        if row.get('type') == u'url' and row.get('idno'):
            book =  Book(gallica_url=row.get('idno'))
            book.add_query_endpoints(endpoints)
            book.query(check_type=False)
            book.deepen_search()
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







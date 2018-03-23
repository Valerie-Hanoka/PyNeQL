#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import *

from pyneql.ontology.book import Book
from pyneql.utils.enum import LanguagesIso6391 as Lang
from pyneql.utils.endpoints import Endpoint

from pyneql.utils.utils import QueryException

import datetime


##################################################
#                 QUERY
##################################################

@raises(QueryException)
def test_book_incomplete():
    """Book - Not enough arguments: Should fail"""
    Book(author="Marie Poppins", query_language=Lang.English)


# Testing Endpoint: dbpedia
def test_book_dbpedia_query_strict_True():
    """Book - dbpedia - : Should pass"""
    book = Book(
        title="A Vindication of the Rights of Woman",
        author="Mary Wollstonecraft",
        endpoints=[Endpoint.dbpedia])
    book.query()

    assert book.attributes


#def test_book_dbpedia_query_strict_False():
#    """Book - dbpedia - strict=False - : Should pass """
#    book = Book(XXX, query_language=Lang.German)
#    book.add_query_endpoint(Endpoint.dbpedia)
#    book.query_builder.set_limit(666)
#    book.query(strict_mode=False)
#    assert u'http://wikidata.dbpedia.org/resource/Q234279' in book.attributes.get(u'owl:sameAs')
#
## Testing Endpoint: dbpedia_fr
#
#def test_book_dbpedia_fr_query_strict_True():
#    """Book - dbpedia_fr - strict=True - : Should pass """
#    book = Book(XXX, query_language=Lang.French)
#    book.add_query_endpoint(Endpoint.dbpedia_fr)
#    book.query(strict_mode=True)
#    assert u'freebase:m.05rj1c' in book.attributes.get(u'owl:sameAs')
#
#
#def test_book_dbpedia_fr_query_strict_False():
#    """Book - dbpedia_fr - strict=False - : Should pass """
#    book = Book(XXX, query_language=Lang.French)
#    book.add_query_endpoint(Endpoint.dbpedia_fr)
#    book.query(strict_mode=False)
#    assert u'freebase:m.0ljm' in book.attributes.get(u'owl:sameAs')
#
#
## Testing Endpoint: wikidata
## def test_book_wikidata_query_strict_True():
##     """Book - wikidata - strict=True - : Should pass """
##     book = Book(XXX, query_language=Lang.Chinese)
##     book.add_query_endpoint(Endpoint.wikidata)
##     book.query(strict_mode=True)
##     assert u'wd:Q17025364' in book.attributes.get(u'owl:sameAs')
##
##
## def test_book_wikidata_query_strict_False():
##     """Book - wikidata - strict=False - : Should pass"""
##     book = Book(XXX, query_language=Lang.Greek_modern)
##     book.add_query_endpoint(Endpoint.wikidata)
##     book.query(strict_mode=False)
##      assert u'wd:Q859' in book.attributes.get(u'owl:sameAs')
#
#
## Testing Endpoint: bnf
#def test_book_bnf_query_strict_True():
#    """Book - bnf - strict=True - : Should pass """
#    book = Book(XXX, query_language=Lang.French)
#    book.add_query_endpoint(Endpoint.bnf)
#    book.query(strict_mode=True)
#    assert u'dbpedia_fr:Simone_de_Beauvoir' in book.attributes.get(u'owl:sameAs')
#
#def test_book_bnf_query_strict_False():
#    """Book - bnf - strict=False - : Should pass """
#    book = Book(XXX, query_language=Lang.French)
#    book.add_query_endpoint(Endpoint.bnf)
#    book.query(strict_mode=False)
#    import pprint; pprint.pprint(book.attributes)
#    assert u'dbpedia_fr:Hannah_Arendt' in book.attributes.get(u'owl:sameAs')
#
## With URL
#
#def test_book_query_URL():
#    """Book - URL query - : Should pass """
#    book = Book(url='http://data.bnf.fr/ark:/12148/cb118905823#foaf:Book')
#    book.add_query_endpoints([Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf])
#    book.query(strict_mode=True)
#    assert u'http://viaf.org/viaf/17218730' in book.attributes.get(u'owl:sameAs')
#
#
## With Gallica URL
#
#
#def test_book_query_URL():
#    """Book - URL query - : Should pass """
#    book = Book(gallica_url=u"http://gallica.bnf.fr/ark:/12148/bpt6k5440566j")
#    book.add_query_endpoints([Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf])
#    book.query(strict_mode=True)
#    assert u'http://viaf.org/viaf/17218730' in book.attributes.get(u'owl:sameAs')
#
#
###################################################
##                 OTHER METHODS
###################################################
#
#def test_book_deepen_search():
#    """Book - find_more_about(): Should pass"""
#    raise NotImplementedError





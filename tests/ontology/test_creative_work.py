#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_creative_work.py is part of the project PyNeQL
Author: Valérie Hanoka

"""


from nose.tools import *

from pyneql.ontology.creative_work import CreativeWork
from pyneql.utils.enum import LanguagesIso6391 as Lang
from pyneql.utils.endpoints import Endpoint

from pyneql.utils.utils import QueryException

##################################################
#                 QUERY
##################################################

@raises(QueryException)
def test_work_incomplete():
    """CreativeWork - Not enough arguments: Should fail"""
    CreativeWork(author="qkdsjfoziej")


# Testing Endpoint: dbpedia
def test_work_dbpedia_query():
    """CreativeWork - dbpedia : Should pass"""

    work1 = CreativeWork(
        title="arXiv",
        author="Paul Ginsparg",
        endpoints=[Endpoint.dbpedia])

    work1.query(strict_mode=True, check_type=True)

    work2 = CreativeWork(
        title="arXiv",
        author="Paul Ginsparg",
        endpoints=[Endpoint.dbpedia])

    work2.query(strict_mode=True, check_type=False)

    work3 = CreativeWork(
        title="arXiv",
        author="Paul Ginsparg",
        endpoints=[Endpoint.dbpedia])

    work3.query(strict_mode=False, check_type=True)

    work4 = CreativeWork(
        title="arXiv",
        author="Paul Ginsparg",
        endpoints=[Endpoint.dbpedia])

    work4.query(strict_mode=False, check_type=False)

    assert work1.attributes
    assert work2.attributes
    assert work3.attributes
    assert work4.attributes


## Testing Endpoint: dbpedia_fr

def test_work_dbpedia_query():
    """CreativeWork - dbpedia_fr : Should pass"""

    work1 = CreativeWork(
        title="Arrival",
        author="ABBA",
        author_is_organisation=True,
        endpoints=[Endpoint.dbpedia_fr],
        query_language=Lang.French)

    work1.query(strict_mode=True, check_type=True)

    work2 = CreativeWork(
        title="Arrival",
        author="ABBA",
        author_is_organisation=True,
        endpoints=[Endpoint.dbpedia_fr],
        query_language=Lang.French)

    work2.query(strict_mode=True, check_type=False)

    work3 = CreativeWork(
        title="Arrival",
        author="ABBA",
        author_is_organisation=True,
        endpoints=[Endpoint.dbpedia_fr],
        query_language=Lang.French)

    work3.query(strict_mode=False, check_type=True)

    work4 = CreativeWork(
        title="Arrival",
        author="ABBA",
        author_is_organisation=True,
        endpoints=[Endpoint.dbpedia_fr],
        query_language=Lang.French)

    work4.query(strict_mode=False, check_type=False)

    assert work1.attributes
    assert work2.attributes
    assert work3.attributes
    assert work4.attributes


# Testing Endpoint: wikidata
def test_work_wikidata_query_strict_True():
    """CreativeWork - wikidata : Should pass """
    work = CreativeWork(
        title=u"凱風快晴",
        author=u"葛飾北斎",
        endpoints=[Endpoint.wikidata],
        query_language=Lang.Japanese)

    work.query(strict_mode=False, check_type=False)
    assert work.attributes


# With URL

def test_work_query_URL():
    """CreativeWork - URL query - : Should pass """
    work = CreativeWork(url='http://www.wikidata.org/entity/Q643347')
    work.add_query_endpoints([Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf])
    work.query(strict_mode=True)
    assert work.attributes

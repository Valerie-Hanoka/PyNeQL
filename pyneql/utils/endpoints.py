#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
endpoints is part of the project PyNeQL
Author: Valérie Hanoka

"""
from aenum import Enum


class Endpoint(Enum):
    """ List of the supported endpoints """

    # Generic information
    dbpedia = u'http://dbpedia.org/sparql'
    dbpedia_fr = u'http://fr.dbpedia.org/sparql'
    wikidata = u'https://query.wikidata.org/sparql'  # u'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

    # Bibliographic information
    bnf = u'http://data.bnf.fr/sparql'

    # Lexical info
    # wordnel =
    # babelnet = u'http://babelnet.org/sparql/'

    # Default Endpoint
    DEFAULT = u'http://dbpedia.org/sparql'



def is_endpoint_multilingual(endpoint):
    """ Some endpoints are multilinguals and requires the language information
    to be given during a query.

    :param endpoint: An endpoint
    :return: True if the endpoint serves multilingual information, False otherwise.
    """
    multilingual_endpoints = [
        Endpoint.dbpedia,
        Endpoint.dbpedia_fr,
        Endpoint.wikidata
        ]
    if endpoint in multilingual_endpoints:
        return True

    return False

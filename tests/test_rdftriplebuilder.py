#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_query_builder.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from nose.tools import *

from pyneql.utils import (
    NameSpaceException
)

from pyneql.rdftriplebuilder import (
    RDFTripletBuilder
)

from pyneql.vocabulary import NameSpace, add_namespace

#---------------------------------------
#          RDF Triples
#---------------------------------------

def test_rdftripletbuilder_base_case():
    """RDFTripletBuilder - Base case, no issues: Should pass """

    rdf = RDFTripletBuilder(
        subject=u"Test",
        predicate=u"<http://purl.org/dc/elements/1.1/title>"
    )
    assert rdf.subject == u'Test'
    assert rdf.object == u'?o'
    assert rdf.predicate == u'dc:title'
    assert rdf.prefixes == [NameSpace.dc]



def test_rdftripletbuilder_check_prefix():
    """RDFTripletBuilder - Prefix checking: Should pass """

    rdf1 = RDFTripletBuilder(
        subject=u"foaf:name",
        predicate=u"<http://purl.org/dc/elements/1.1/title>"
    )
    assert rdf1.subject == u'foaf:name'
    assert rdf1.object == u'?o'
    assert rdf1.predicate == u'dc:title'

    truth = [NameSpace.dc, NameSpace.foaf]
    computed = rdf1.prefixes
    diff = len(set(computed) - set(truth))
    assert not diff


def test_rdftripletbuilder_prefix_normalization():
    """RDFTripletBuilder - Prefix normalisation: Should pass """

    rdf2 = RDFTripletBuilder(
        prefixes=[
            " t3st_1234  : <http://foo.org/bar/1.1/buz.owl#>  .",
            "xsd: <http://www.w3.org/2001/XMLSchema#>"])

    assert rdf2.subject == u'?s'
    assert rdf2.object == u'?o'
    assert rdf2.predicate == u'?p'

    add_namespace("t3st_1234", "http://foo.org/bar/1.1/buz.owl#")
    truth = [NameSpace('http://foo.org/bar/1.1/buz.owl#'), NameSpace.xsd]
    computed = rdf2.prefixes
    diff = set(computed) - set(truth)
    assert not len(diff)


@raises(NameSpaceException)
def test_rdftripletbuilder_prefix_inconsistencies1():
        """RDFTripletBuilder - Inconsistency between
        the vocabulary and a given namespace: Should fail """

        # "t3st_1234" is not in the vocabulary but "http://www.w3.org/2001/XMLSchema#" is.
        rdf = RDFTripletBuilder(prefixes=["t3st_1234: <http://www.w3.org/2001/XMLSchema#>"])


@raises(NameSpaceException)
def test_rdftripletbuilder_prefix_inconsistencies2():
        """RDFTripletBuilder - Inconsistency between
        the vocabulary and a given namespace (the other way around): Should fail """

        rdf = RDFTripletBuilder(prefixes=["xsd: <http://foo.org/bar/1.1/buz.owl#>"])



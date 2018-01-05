#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_query_builder.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from nose.tools import *

from pyneql.utils.utils import NameSpaceException
from pyneql.query.rdftriple import RDFTriple
from pyneql.utils.enum import LanguagesIso6391 as Lang
from pyneql.utils.namespace import NameSpace, add_namespace

#---------------------------------------
#          RDF Triples
#---------------------------------------

def test_rdftripletbuilder_base_case():
    """RDFTriple - Base case, no issues: Should pass """

    rdf = RDFTriple(
        subject=u"Test",
        predicate=u"<http://purl.org/dc/elements/1.1/title>"
    )
    assert rdf.subject == u'Test'
    assert rdf.object == u'?o_%i' % rdf.class_counter
    assert rdf.predicate == u'dc:title'
    assert rdf.prefixes == [NameSpace.dc]


def test_rdftripletbuilder_check_prefix():
    """RDFTriple - Prefix checking: Should pass """

    rdf1 = RDFTriple(
        subject=u"foaf:name",
        predicate=u"<http://purl.org/dc/elements/1.1/title>"
    )
    assert rdf1.subject == u'foaf:name'
    assert rdf1.object == u'?o_%i' % rdf1.class_counter
    assert rdf1.predicate == u'dc:title'

    truth = [NameSpace.dc, NameSpace.foaf]
    computed = rdf1.prefixes
    diff = len(set(computed) - set(truth))
    assert not diff


def test_rdftripletbuilder_prefix_normalization():
    """RDFTriple - Prefix normalisation: Should pass """

    rdf2 = RDFTriple(
        prefixes=[
            " t3st_1234  : <http://foo.org/bar/1.1/buz.owl#>  .",
            "xsd: <http://www.w3.org/2001/XMLSchema#>"])

    assert rdf2.subject == u'?s_%i' % rdf2.class_counter
    assert rdf2.object == u'?o_%i' % rdf2.class_counter
    assert rdf2.predicate == u'?p_%i' % rdf2.class_counter

    add_namespace("t3st_1234", "http://foo.org/bar/1.1/buz.owl#")
    truth = [NameSpace('http://foo.org/bar/1.1/buz.owl#'), NameSpace.xsd]
    computed = rdf2.prefixes
    diff = set(computed) - set(truth)
    assert not len(diff)


def test_rdftripletbuilder_add_prefixes_after_creation():
    """RDFTriple - RDF prefix declaration after creation: should pass"""

    test1 = RDFTriple(object=u'"foo"')
    test1.add_prefixes([NameSpace.dawgt, "barbarbar: <http://bar.org/bar/bar/>"])
    test1.subject = u'barbarbar:foofoofoo'

    assert test1.__str__() == u'barbarbar:foofoofoo ?p_%i "foo" .' % test1.class_counter
    diff = set(test1.prefixes) - set([NameSpace.dawgt, NameSpace.barbarbar])
    assert not len(diff)



@raises(NameSpaceException)
def test_rdftripletbuilder_prefix_inconsistencies1():
        """RDFTriple - Inconsistency between
        the vocabulary and a given namespace: Should fail """

        # "t3st_1234" is not in the vocabulary but "http://www.w3.org/2001/XMLSchema#" is.
        rdf = RDFTriple(prefixes=["t3st_1234: <http://www.w3.org/2001/XMLSchema#>"])


@raises(NameSpaceException)
def test_rdftripletbuilder_prefix_inconsistencies2():
        """RDFTriple - Inconsistency between
        the vocabulary and a given namespace (the other way around): Should fail """

        rdf = RDFTriple(prefixes=["xsd: <http://foo.org/bar/1.1/buz.owl#>"])


@raises(NameSpaceException)
def test_rdftripletbuilder_add_prefixes_after_creation_inconsistencies():
    """RDFTriple - bad RDF prefix declaration: should fail"""

    test1 = RDFTriple(object=u'"foo"')
    test1.add_prefix("prefix: bar, abbr: <http://bar.org/bar/bar/>")


def test_rdftripletbuilder_literal_language():
    """RDFTriple - Literal with language: should pass"""

    test1 = RDFTriple(object=u'"Clinton"', language=Lang.Albanian)
    assert test1.__str__(with_language=True) == u'?s_%i ?p_%i "Clinton"@sq .' % (test1.class_counter, test1.class_counter)
    assert test1.__str__() == u'?s_%i ?p_%i "Clinton" .' % (test1.class_counter, test1.class_counter)

    test2 = RDFTriple(object=u'foaf:crap', language=Lang.Albanian)
    assert test2.__str__(with_language=True) == test2.__str__()

    test3 = RDFTriple(object="?var", language=Lang.Albanian)
    assert test3.__str__(with_language=True) == test3.__str__()

    test4 = RDFTriple(object=u'"1924"', language=Lang.Albanian)
    assert test4.__str__(with_language=True) == test4.__str__()


def test_get_variables():
    """RDFTriple - Literal with language: should pass"""

    rdf = RDFTriple()
    truth = set([u'?%s_%i' % (role, rdf.class_counter) for role in "sop"])
    diff = set(rdf.get_variables()) - truth
    assert not len(diff)
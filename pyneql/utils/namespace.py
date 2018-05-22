#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
namespace.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
from pyneql.log.loggingsetup import (
    setup_logging,
)

from pyneql.utils.utils import NameSpaceException

from aenum import Enum, extend_enum
import re


RE_NAMESPACE_CHECKER = re.compile(
    '^\s*(?P<abbr>\w+)\s*:\s*<(?P<uri>http://[^>\s]+)>[\s\.]*$')

RE_URI = re.compile(
    '^(?P<uri>http://.+)(?P<sep>[/#])(?P<attr>[^^#]+)\s*$')


class NameSpace(Enum):
    """
    Common SPARQL prefixes.
    See also https://prefix.cc/
    """
    akt = u'http://www.aktors.org/ontology/portal#'
    akts = u'http://www.aktors.org/ontology/support #'
    bd = u'http://www.bigdata.com/rdf#'
    bds = u'http://www.bigdata.com/rdf/search#'
    bibo = u'http://purl.org/ontology/bibo/'
    bio = u'http://vocab.org/bio/0.1/'
    bnf_onto = u'http://data.bnf.fr/ontology/bnf-onto/'
    bnfroles = u'http://data.bnf.fr/vocabulary/roles/'
    category = u'http://dbpedia.org/resource/Category:'
    category_fr = u'http://fr.dbpedia.org/resource/Catégorie:'
    dawgt = u'http://www.w3.org/2001/sw/DataAccess/tests/test-dawg#'
    dbc = u'http://dbpedia.org/resource/Category:'
    dbo = u'http://dbpedia.org/ontology/'
    dbp = u'http://dbpedia.org/property/'
    dbpedia = u'http://dbpedia.org/resource/'
    dbpedia_cs = u'http://cs.dbpedia.org/resource/'
    dbpedia_de = u'http://de.dbpedia.org/resource/'
    dbpedia_el = u'http://el.dbpedia.org/resource/'
    dbpedia_es = u'http://es.dbpedia.org/resource/'
    dbpedia_fr = u'http://fr.dbpedia.org/resource/'
    dbpedia_it = u'http://it.dbpedia.org/resource/'
    dbpedia_ja = u'http://ja.dbpedia.org/resource/'
    dbpedia_ko = u'http://ko.dbpedia.org/resource/'
    dbpedia_nl = u'http://nl.dbpedia.org/resource/'
    dbpedia_owl = u'http://dbpedia.org/ontology/'
    dbpedia_pl = u'http://pl.dbpedia.org/resource/'
    dbpedia_pt = u'http://pt.dbpedia.org/resource/'
    dbpedia_ru = u'http://ru.dbpedia.org/resource/'
    dbpprop = u'http://dbpedia.org/property/'
    dbr = u'http://dbpedia.org/resource/'
    dc = u'http://purl.org/dc/elements/1.1/'
    dcmi_box = u'http://dublincore.org/documents/dcmi-box/'
    dcmitype = u'http://purl.org/dc/dcmitype/'
    dct = u'http://purl.org/dc/terms/'
    dcterms = u'http://purl.org/dc/terms/'
    dul = u'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#'
    fabio = u'http://purl.org/spar/fabio/'
    fn = u'http://www.w3.org/2005/xpath-functions/#'
    foaf = u'http://xmlns.com/foaf/0.1/'
    frbr_rda = u'http://rdvocab.info/uri/schema/FRBRentitiesRDA/'
    freebase = u'http://rdf.freebase.com/ns/'
    gas = u'http://www.bigdata.com/rdf/gas#'
    genremus = u'http://data.bnf.fr/vocabulary/musical-genre/'
    geo = u'http://www.w3.org/2003/01/geo/wgs84_pos#'
    geonames = u'http://www.geonames.org/ontology#'
    georss = u'http://www.georss.org/georss/'
    go = u'http://purl.org/obo/owl/GO#'
    hint = u'http://www.bigdata.com/queryHints#'
    id = u'http://wordnet.rkbexplorer.com/id/'
    ign = u'http://data.ign.fr/ontology/topo.owl#'
    insee = u'http://rdf.insee.fr/geo/'
    isni = u'http://isni.org/ontology#'
    ldp = u'http://www.w3.org/ns/ldp#'
    marcrel = u'http://id.loc.gov/vocabulary/relators/'
    math = u'http://www.w3.org/2000/10/swap/math#'
    mesh = u'http://purl.org/commons/record/mesh/'
    mf = u'http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#'
    mo = u'http://musicontology.com/'
    nci = u'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#'
    obo = u'http://www.geneontology.org/formats/oboInOwl#'
    ogc = u'http://www.opengis.net/'
    ogcgml = u'http://www.opengis.net/ont/gml#'
    ogcgs = u'http://www.opengis.net/ont/geosparql#'
    ogcgsf = u'http://www.opengis.net/def/function/geosparql/'
    ogcgsr = u'http://www.opengis.net/def/rule/geosparql/'
    ogcsf = u'http://www.opengis.net/ont/sf#'
    opencyc = u'http://sw.opencyc.org/2008/06/10/concept/'
    ore = u'http://www.openarchives.org/ore/terms/'
    owl = u'http://www.w3.org/2002/07/owl#'
    p = u'http://www.wikidata.org/prop/'
    pq = u'http://www.wikidata.org/prop/qualifier/'
    pqn = u'http://www.wikidata.org/prop/qualifier/value-normalized/'
    pqv = u'http://www.wikidata.org/prop/qualifier/value/'
    pr = u'http://www.wikidata.org/prop/reference/'
    prn = u'http://www.wikidata.org/prop/reference/value-normalized/'
    product = u'http://www.buy.com/rss/module/productV2/'
    prop_fr = u'http://fr.dbpedia.org/property/'
    protseq = u'http://purl.org/science/protein/bysequence/'
    prov = u'http://www.w3.org/ns/prov#'
    prv = u'http://www.wikidata.org/prop/reference/value/'
    ps = u'http://www.wikidata.org/prop/statement/'
    psn = u'http://www.wikidata.org/prop/statement/value-normalized/'
    psv = u'http://www.wikidata.org/prop/statement/value/'
    rdagroup1elements = u'http://rdvocab.info/Elements/'
    rdagroup2elements = u'http://rdvocab.info/ElementsGr2/'
    rdarelationships = u'http://rdvocab.info/RDARelationshipsWEMI/'
    rdf = u'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    rdfa = u'http://www.w3.org/ns/rdfa#'
    rdfdf = u'http://www.openlinksw.com/virtrdf-data-formats#'
    rdfs = u'http://www.w3.org/2000/01/rdf-schema#'
    sc = u'http://purl.org/science/owl/sciencecommons/'
    schema = u'http://schema.org/'
    schemaorg = u'http://schema.org/'
    scovo = u'http://purl.org/NET/scovo#'
    sd = u'http://www.w3.org/ns/sparql-service-description#'
    sioc = u'http://rdfs.org/sioc/ns#'
    skos = u'http://www.w3.org/2004/02/skos/core#'
    template = u'http://dbpedia.org/resource/Template:'
    template_fr = u'http://fr.dbpedia.org/resource/Template:'
    umbel_ac = u'http://umbel.org/umbel/ac/'
    umbel_sc = u'http://umbel.org/umbel/sc/'
    units = u'http://dbpedia.org/units/'
    vcard = u'http://www.w3.org/2001/vcard-rdf/3.0#'
    vcard2006 = u'http://www.w3.org/2006/vcard/ns#'
    virtcxml = u'http://www.openlinksw.com/schemas/virtcxml#'
    virtrdf = u'http://www.openlinksw.com/schemas/virtrdf#'
    void = u'http://rdfs.org/ns/void#'
    wd = u'http://www.wikidata.org/entity/'
    wdata = u'http://www.wikidata.org/wiki/Special:EntityData/'
    wdno = u'http://www.wikidata.org/prop/novalue/'
    wdref = u'http://www.wikidata.org/reference/'
    wds = u'http://www.wikidata.org/entity/statement/'
    wdt = u'http://www.wikidata.org/prop/direct/'
    wdt_o = u'http://www.wikidata.org/ontology#'
    wdv = u'http://www.wikidata.org/value/'
    wiki_fr = u'http://fr.wikipedia.org/wiki/'
    wikibase = u'http://wikiba.se/ontology#'
    wikicompany = u'http://dbpedia.openlinksw.com/wikicompany/'
    wikidata = u'http://www.wikidata.org/entity/'
    xf = u'http://www.w3.org/2004/07/xpath-functions'
    xml = u'http://www.w3.org/XML/1998/namespace'
    xsd = u'http://www.w3.org/2001/XMLSchema#'
    xsl10 = u'http://www.w3.org/XSL/Transform/1.0'
    xsl1999 = u'http://www.w3.org/1999/XSL/Transform'
    xslwd = u'http://www.w3.org/TR/WD-xsl'
    yago = u'http://dbpedia.org/class/yago/'
    yago_res = u'http://mpii.de/yago/resource/'



# def get_uri_last_part(uri):
#     """
#     Returns only the last part of an URI. E.g:
#     >>> get_uri_last_part("http://rdvocab.info/ElementsGr2/dateOfDeath")
#     >>> dateOfDeath
#     :param uri: An URI
#     :return: the last part of the URI
#     """
#     return uri.rpartition('/')[-1]

def get_shortened_uri(uri):
    """ Return a shortened URI if the namespace is known.

    >>> get_shortened_uri("http://xmlns.com/foaf/0.1/surname")
    >>> "foaf:surname"

    """
    is_uri = RE_URI.match(uri)
    if is_uri:
        try:
            prefix = NameSpace(u'%s%s' % (is_uri.group('uri'), is_uri.group('sep')))
            uri = u'%s:%s' % (prefix.name, is_uri.group('attr'))
        except ValueError:
            pass
    return uri

def get_expended_uri(uri):
    """Return the expanded form of a short URI if the namespace is known.

    >>> get_expended_uri("foaf:surname")
    >>> "http://xmlns.com/foaf/0.1/surname"

    :param uri: the URI to expand.
    :return: the long URI if it exists, else None
    """
    (pref, _, post) = uri.rpartition(':')
    if pref:
        corresponding_namespace = NameSpace.__members__.get(pref, None)
        if corresponding_namespace:
            return "%s%s" % (corresponding_namespace.value, post)
    return


def decompose_prefix(prefix):
    """
    Decomposes a prefix in its parts.

    :Example:

    ``gn: <http://www.geonames.org/ontology#>`` will be decomposed in:

    - the abbreviation ``gn``
    - the url ``http://www.geonames.org/ontology#``

    :param prefix: A well-formed SPARQL prefix
    :return: A parsed SPARQL prefix: (abbreviation, url)
    :raises NameSpaceException: The prefix is ill-formed
    """
    is_well_formed = RE_NAMESPACE_CHECKER.match(prefix)

    if is_well_formed:
        abbr = is_well_formed.group(u"abbr")
        url = is_well_formed.group(u"uri")
        return abbr, url
    else:
        raise NameSpaceException(u"The prefix %s is not well formed." % prefix)


def get_consistent_namespace(abbreviation, namespace):
    """
    Given an abbreviation (e.g.: "foaf") and a namespace
    (e.g.: "http://xmlns.com/foaf/0.1/") we check that the
    mapping abbreviation: namespace is in the vocabulary.
    This function raises a :class:`NameSpaceException` if (at least)
    one of the element is in the vocabulary but the other does
    not corresponds to what is given in the vocabulary.
    Returns the corresponding NameSpace if it exists or None.

    :param abbreviation: A SPARQL PREFIX abbreviation (e.g.: "foaf")
    :param namespace: A SPARQL PREFIX namespace (e.g.: "http://xmlns.com/foaf/0.1/")
    :return: The corresponding NameSpace if it exists or None
    :raises NameSpaceException: The prefix cannot be dynamically added to the vocabulary
    """

    # Getting the voc.NameSpace corresponding to the namespace
    try:
        abbr_ns = NameSpace(namespace)
    except ValueError:
        abbr_ns = None

    # Getting the voc.NameSpace corresponding to the abbreviation
    ns_abbr = NameSpace.__members__.get(abbreviation)

    if not (ns_abbr or abbr_ns):
        return None  # Neither element can be found in the vocabulary

    if ns_abbr and abbr_ns and (abbr_ns == ns_abbr):
        return abbr_ns  # It's a match ! We return the corresponding voc.NameSpace

    raise NameSpaceException(
        u"In the standard vocabulary, %s does not correspond to %s."
        u"This could lead to inconsistencies."
        u"Check your prefixes again or contact the author." % (abbreviation, namespace))


def add_namespace(prefix, url):
    """
    Add an element to NameSpace enumeration, and returns it.

    :param prefix: The name of the NameSpace to be added
    :param url: The url of the NameSpace to be added
    :return: The added NameSpace element
    """
    setup_logging()
    extend_enum(NameSpace, prefix, url)
    logging.info(u"NameSpace %s: %s added to the list of name spaces." % (prefix, url))
    return NameSpace(url)

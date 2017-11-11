#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vocabulary.py is part of the project PyNeQL
Author: Valérie Hanoka

"""
from utils import (
    NameSpaceException,
)

from aenum import Enum, extend_enum


class NameSpace(Enum):
    """Common SPARQL prefixes."""

    dbpedia_cs = u'http://cs.dbpedia.org/resource/'
    bnf_onto = u'http://data.bnf.fr/ontology/bnf-onto/'
    genremus = u'http://data.bnf.fr/vocabulary/musical-genre/'
    bnfroles = u'http://data.bnf.fr/vocabulary/roles/'
    ign = u'http://data.ign.fr/ontology/topo.owl#'
    wikicompany = u'http://dbpedia.openlinksw.com/wikicompany/'
    yago = u'http://dbpedia.org/class/yago/'
    dbpedia_owl = u'http://dbpedia.org/ontology/'
    dbpprop = u'http://dbpedia.org/property/'
    dbpedia = u'http://dbpedia.org/resource/'
    category = u'http://dbpedia.org/resource/Category:'
    template = u'http://dbpedia.org/resource/Template:'
    units = u'http://dbpedia.org/units/'
    dbpedia_de = u'http://de.dbpedia.org/resource/'
    dcmi_box = u'http://dublincore.org/documents/dcmi-box/'
    dbpedia_el = u'http://el.dbpedia.org/resource/'
    dbpedia_es = u'http://es.dbpedia.org/resource/'
    prop_fr = u'http://fr.dbpedia.org/property/'
    dbpedia_fr = u'http://fr.dbpedia.org/resource/'
    category_fr = u'http://fr.dbpedia.org/resource/Catégorie:'
    template_fr = u'http://fr.dbpedia.org/resource/Template:'
    wiki_fr = u'http://fr.wikipedia.org/wiki/'
    marcrel = u'http://id.loc.gov/vocabulary/relators/'
    isni = u'http://isni.org/ontology#'
    dbpedia_it = u'http://it.dbpedia.org/resource/'
    dbpedia_ja = u'http://ja.dbpedia.org/resource/'
    dbpedia_ko = u'http://ko.dbpedia.org/resource/'
    yago_res = u'http://mpii.de/yago/resource/'
    mo = u'http://musicontology.com/'
    nci = u'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#'
    dbpedia_nl = u'http://nl.dbpedia.org/resource/'
    dbpedia_pl = u'http://pl.dbpedia.org/resource/'
    dbpedia_pt = u'http://pt.dbpedia.org/resource/'
    scovo = u'http://purl.org/NET/scovo#'
    mesh = u'http://purl.org/commons/record/mesh/'
    dcmitype = u'http://purl.org/dc/dcmitype/'
    dc = u'http://purl.org/dc/elements/1.1/'
    dcterms = u'http://purl.org/dc/terms/'
    go = u'http://purl.org/obo/owl/GO#'
    bibo = u'http://purl.org/ontology/bibo/'
    sc = u'http://purl.org/science/owl/sciencecommons/'
    protseq = u'http://purl.org/science/protein/bysequence/'
    freebase = u'http://rdf.freebase.com/ns/'
    insee = u'http://rdf.insee.fr/geo/'
    void = u'http://rdfs.org/ns/void#'
    sioc = u'http://rdfs.org/sioc/ns#'
    rdagroup1elements = u'http://rdvocab.info/Elements/'
    rdagroup2elements = u'http://rdvocab.info/ElementsGr2/'
    rdarelationships = u'http://rdvocab.info/RDARelationshipsWEMI/'
    frbr_rda = u'http://rdvocab.info/uri/schema/FRBRentitiesRDA/'
    dbpedia_ru = u'http://ru.dbpedia.org/resource/'
    schemaorg = u'http://schema.org/'
    opencyc = u'http://sw.opencyc.org/2008/06/10/concept/'
    umbel_ac = u'http://umbel.org/umbel/ac/'
    umbel_sc = u'http://umbel.org/umbel/sc/'
    bio = u'http://vocab.org/bio/0.1/'
    product = u'http://www.buy.com/rss/module/productV2/'
    obo = u'http://www.geneontology.org/formats/oboInOwl#'
    geonames = u'http://www.geonames.org/ontology#'
    georss = u'http://www.georss.org/georss/'
    ore = u'http://www.openarchives.org/ore/terms/'
    ogc = u'http://www.opengis.net/'
    ogcgsf = u'http://www.opengis.net/def/function/geosparql/'
    ogcgsr = u'http://www.opengis.net/def/rule/geosparql/'
    ogcgs = u'http://www.opengis.net/ont/geosparql#'
    ogcgml = u'http://www.opengis.net/ont/gml#'
    ogcsf = u'http://www.opengis.net/ont/sf#'
    virtcxml = u'http://www.openlinksw.com/schemas/virtcxml#'
    virtrdf = u'http://www.openlinksw.com/schemas/virtrdf#'
    rdfdf = u'http://www.openlinksw.com/virtrdf-data-formats#'
    rdf = u'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    xsl1999 = u'http://www.w3.org/1999/XSL/Transform'
    rdfs = u'http://www.w3.org/2000/01/rdf-schema#'
    math = u'http://www.w3.org/2000/10/swap/math#'
    xsd = u'http://www.w3.org/2001/XMLSchema#'
    dawgt = u'http://www.w3.org/2001/sw/DataAccess/tests/test-dawg#'
    mf = u'http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#'
    vcard = u'http://www.w3.org/2001/vcard-rdf/3.0#'
    owl = u'http://www.w3.org/2002/07/owl#'
    geo = u'http://www.w3.org/2003/01/geo/wgs84_pos#'
    skos = u'http://www.w3.org/2004/02/skos/core#'
    xf = u'http://www.w3.org/2004/07/xpath-functions'
    fn = u'http://www.w3.org/2005/xpath-functions/#'
    vcard2006 = u'http://www.w3.org/2006/vcard/ns#'
    xslwd = u'http://www.w3.org/TR/WD-xsl'
    xml = u'http://www.w3.org/XML/1998/namespace'
    xsl10 = u'http://www.w3.org/XSL/Transform/1.0'
    ldp = u'http://www.w3.org/ns/ldp#'
    rdfa = u'http://www.w3.org/ns/rdfa#'
    sd = u'http://www.w3.org/ns/sparql-service-description#'
    foaf = u'http://xmlns.com/foaf/0.1/'


def _get_consistent_namespace(abbreviation, namespace):
    """ Given an abbreviation (e.g.: "foaf") and a namespace
    (e.g.: "http://xmlns.com/foaf/0.1/") we check that the
    mapping abbreviation: namespace is in the vocabulary.
    This function raises a NameSpaceException if (at least)
    one of the element is in the vocabulary but the other does
    not corresponds to what is given in the vocabulary."""

    # Getting the voc.NameSpace corresponding to the namespace
    try:
        abbr_ns = NameSpace(namespace)
    except ValueError:
        abbr_ns = None

    # Getting the voc.NameSpace corresponding to the abbreviation
    ns_abbr = NameSpace.__members__.get(abbreviation)

    if not (ns_abbr or abbr_ns):
        return False  # Neither element can be found in the vocabulary

    if ns_abbr and abbr_ns and (abbr_ns == ns_abbr):
        return abbr_ns  # It's a match ! We return the corresponding voc.NameSpace

    raise NameSpaceException(
        "In the stadard vocabulary, %s does not correspond to %s."
        "This could lead to inconsistencies."
        "Check your prefixes again or contact the author." % (abbreviation, namespace))


def add_namespace(prefix, url):
    extend_enum(NameSpace, prefix, url)

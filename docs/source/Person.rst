Person
=========================================

The class ``Person`` is designed to retrieve all the information about a given person.
For the moment, it is possible to launch a query with either:

- her/his full_name;
- her/his first_name *and* last_name;
- the URL/URI corresponding to the person.


.. image:: ../../illustration_delimitante.png
  :width: 600
  :alt: ⚓


Looking for a Person
---------------------


Basic search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We want to find `bell hooks <https://en.wikipedia.org/wiki/Bell_hooks>`_
on the following endpoints:

- `DBpedia <http://dbpedia.org/sparql>`_,
- `Wikidata <https://query.wikidata.org/sparql>`_,
- `BnF <http://data.bnf.fr/sparql>`_,
- `French DBpedia <http://fr.dbpedia.org/sparql>`_

::

    from pyneql.ontology.person import Person
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

Once the query is sent, the result information is stored in the object's
``attributes`` dictionary

>>> len(bell_hooks.attributes)
15

The content of the result set is as follows::

    {
        'bnf_onto:firstYear': '1952',
         'foaf:depiction': {'http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg',
                            'http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg?width=300',
                            'https://upload.wikimedia.org/wikipedia/commons/7/7b/Bellhooks.jpg'},
         'foaf:familyName': 'hooks',
         'foaf:gender': 'female',
         'foaf:givenName': 'bell',
         'foaf:name': 'bell hooks',
         'foaf:page': 'http://data.bnf.fr/12519986/bell_hooks/',
         'owl:sameAs': {'dbpedia_fr:Bell_hooks',
                        'http://data.bnf.fr/ark:/12148/cb12519986q#about',
                        'http://data.bnf.fr/ark:/12148/cb12519986q#foaf:Person',
                        'http://viaf.org/viaf/79115934'},
         'rdagroup2elements:biographicalInformation': 'Essayiste et enseignante. - '
                                                      'Militante féminisme et contre '
                                                      'la ségragation raciale. - '
                                                      'Fondatrice, en 2014, du bell '
                                                      'hooks Institute, Berea College '
                                                      '(Ky., États-Unis). - Pseudonyme '
                                                      'de Gloria Jean Watkins',
         'rdagroup2elements:countryAssociatedWithThePerson': 'http://id.loc.gov/vocabulary/countries/xxu',
         'rdagroup2elements:fieldOfActivityOfThePerson': {'Sciences sociales. '
                                                          'Sociologie',
                                                          'http://dewey.info/class/300/'},
         'rdagroup2elements:languageOfThePerson': 'http://id.loc.gov/vocabulary/iso639-2/eng',
         'rdf:type': 'foaf:Person',
         'skos:exactMatch': 'http://data.bnf.fr/ark:/12148/cb12519986q#about',
         'validated': 1}
    }


Extended search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the element we are looking for is ubiquitous in the Semantic Web, we may
want to search further. The function ``find_more_about()`` is doing that.
Before the execution of the function ``find_more_about()``, we had 15 RDF predicates having values for bell hooks:
E
This feature just takes the URIs of the first result set which identifies the
same person (identity predicates ``skos:exactMatch``, ``owl:sameAs``)
and retreive the RDF triples associated to those URIs.

>>> bell_hooks.find_more_about()
>>> len(bell hooks.attributes)
223

*N.B.: The numbers of attributes given here for this example are susceptible to variations.*

For our example, the (truncated) content of the result set is as follows::

    {
        'dbo:birthDate': {'1952-09-25+02:00', '1952-9-25', '1952-09-25'},
     'dbo:birthName': {'Gloria Jean Watkins _(@fr)', 'Gloria Jean Watkins _(@en)'},
     'dbo:birthPlace': {'http://dbpedia.org/resource/Hopkinsville,_Kentucky',
                        'http://fr.dbpedia.org/resource/Hopkinsville',
                        'http://fr.dbpedia.org/resource/États-Unis'},
     'dbo:birthYear': '1952',
     'dbo:bnfId': {'12519986q'},
     'dbo:knownFor': {'http://dbpedia.org/resource/Activism',
                      'http://dbpedia.org/resource/Feminism'},
     'dbo:occupation': {'http://dbpedia.org/resource/Bell_hooks__1',
                        'http://fr.dbpedia.org/resource/Intellectuelle'},
     'dbo:sudocId': {'03444453X'},
     'dbo:thumbnail': {'http://commons.wikimedia.org/wiki/Special:FilePath/Bell_hooks,_October_2014.jpg?width=300',
                       'http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg?width=300'},
     'dbo:thumbnailCaption': {'bell hooks en novembre 2009'},
     'dbo:viafId': {'79115934'},
     'dbo:wikiPageExternalLink': {'http://ascentmagazine.com/articles.aspx?articleID=133&page=read&subpage=past&issueID=24',
                                  'http://bombmagazine.org/article/1789/bell-hooks',
                                  'http://digitalcommons.law.yale.edu/cgi/viewcontent.cgi?article=1044&context=yjlf',
                                  'http://digitalcommons.law.yale.edu/cgi/viewcontent.cgi?article=1045&context=yjlf',
                                  'http://dx.doi.org/10.1080/09502389300490051',
                                  'http://dx.doi.org/10.1353/aph.0.0087',
                                  'http://dx.doi.org/10.1353/aph.2012.0109',
                                  'http://dx.doi.org/10.1353/pmc.1990.0004',
                                  'http://dx.doi.org/10.2307/1394725',
                                  'http://dx.doi.org/10.2307/2931578',
                                  'http://dx.doi.org/10.2307/2935186',
                                  'http://dx.doi.org/10.2307/2935286',
                                  'http://dx.doi.org/10.2307/2935451',
                                  'http://dx.doi.org/10.2307/3041692',
                                  'http://dx.doi.org/10.2307/4177045',
                                  'http://eric.ed.gov/?q=EJ425141&id=EJ425141',
                                  'http://heinonline.org/HOL/LandingPage?handle=hein.journals/yjfem4&div=6&id=&page=',
                                  'http://heinonline.org/HOL/LandingPage?handle=hein.journals/yjfem4&div=7&id=&page=',
                                  'http://www.allaboutbell.com/',
                                  'http://www.artpapers.org/',
                                  'http://www.booknotes.org/Watch/67753-1/bell+hooks.aspx',
                                  'http://www.britannica.com/eb/article-9002957/bell-hooks',
                                  'http://www.c-spanvideo.org/program/InDepthw',
                                  'http://www.com.washington.edu/Program/publicscholarship/ps_marwick.pdf',
                                  'http://www.feminish.com/wp-content/uploads/2012/08/bell-hooks-Selling-Hot-Pussy-representation-of-black-womens-sexuality.pdf',
                                  'http://www.frontpagemag.com/Articles/Printable.asp?ID=138',
                                  'http://www.jstor.org/stable/20866297',
                                  'http://www.jstor.org/stable/25797204',
                                  'http://www.jstor.org/stable/3175025',
                                  'http://www.jstor.org/stable/40003500',
                                  'http://www.jstor.org/stable/40425413',
                                  'http://www.library.ucsb.edu/libwaves/mar00/hooks.html',
                                  'http://www.lionsroar.com/author/bell-hooks/',
                                  'http://www.melanine.org/article.php3?id_article=166',
                                  'http://www.msmagazine.com/archive.asp',
                                  'http://www.realchangenews.org/archive3/2005_03_09/current/interview.html',
                                  'http://www.sas.upenn.edu/African_Studies/Articles_Gen/Postmodern_Blackness_18270.html',
                                  'http://www.shambhalasun.com/Archives/Columnists/Hooks/hooks.htm',
                                  'http://www.soaw.org/new/article.php?id=910',
                                  'http://www.southendpress.org/authors/46',
                                  'http://www.synaptic.bc.ca/ejournal/hooks.htm',
                                  'http://www.wholeterrain.org/bio.cfm?Contributor_ID=198',
                                  'http://www.zmag.org/ZMag/articles/dec95hooks.htm',
                                  'https://litnorteamericanaffyl.files.wordpress.com/2009/05/an-aesthetic-of-blackness.pdf'},
     'foaf:depiction': {'http://commons.wikimedia.org/wiki/Special:FilePath/Bell_hooks,_October_2014.jpg',
                        'http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg',
                        'http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg?width=300',
                        'https://upload.wikimedia.org/wikipedia/commons/7/7b/Bellhooks.jpg'},
     'foaf:familyName': {'hooks'},
     'foaf:gender': {'female', 'female _(@en)'},
     'foaf:givenName': {'bell'},
     'foaf:isPrimaryTopicOf': {'http://en.wikipedia.org/wiki/Bell_hooks',
                               'http://fr.wikipedia.org/wiki/Bell_hooks'},
     'foaf:name': {'bell hooks', 'bell hooks _(@fr)', 'bell hooks _(@en)'},
     'foaf:nick': {'bell hooks _(@fr)'},
     'foaf:page': {'http://data.bnf.fr/12519986/bell_hooks/'},
     'http://purl.org/linguistics/gold/hypernym': 'http://dbpedia.org/resource/Author',
     'http://purl.org/voc/vrank#hasRank': {'nodeID://b27429442',
                                           'nodeID://b5705506'},
     'http://www.wikidata.org/prop/direct-normalized/BnF_ID_(P268)': 'http://data.bnf.fr/ark:/12148/cb12519986q',
     'http://www.wikidata.org/prop/direct-normalized/FAST_ID_(P2163)': 'http://id.worldcat.org/fast/1801024',
     'http://www.wikidata.org/prop/direct-normalized/Freebase_ID_(P646)': 'http://g.co/kg/m/01cj42',
     'http://www.wikidata.org/prop/direct-normalized/GND_ID_(P227)': 'http://d-nb.info/gnd/11933447X',
     'http://www.wikidata.org/prop/direct-normalized/Library_of_Congress_authority_ID_(P244)': 'http://id.loc.gov/authorities/names/n82203435',
     'http://www.wikidata.org/prop/direct-normalized/NDL_Auth_ID_(P349)': 'http://id.ndl.go.jp/auth/ndlna/00544810',
     'http://www.wikidata.org/prop/direct-normalized/National_Thesaurus_for_Author_Names_ID_(P1006)': 'http://data.bibliotheken.nl/id/thes/p071042342',
     'http://www.wikidata.org/prop/direct-normalized/SELIBR_(P906)': 'https://libris.kb.se/resource/auth/374125',
     'http://www.wikidata.org/prop/direct-normalized/SUDOC_authorities_(P269)': 'https://www.idref.fr/03444453X/id',
     'http://www.wikidata.org/prop/direct-normalized/VIAF_ID_(P214)': 'https://viaf.org/viaf/79115934',
     'http://www.wikidata.org/prop/direct/http://www.wikidata.org/prop/direct/P5008': 'http://www.wikidata.org/entity/Q24909800',
     'http://www.wikidata.org/prop/http://www.wikidata.org/prop/P5008': 'http://www.wikidata.org/entity/statement/Q259507-9c0e4970-4d12-f6e2-10cf-81f15112be65',
     'owl:sameAs': {'dbpedia_fr:Bell_hooks',
                    'http://d-nb.info/gnd/11933447X',
                    'http://data.bnf.fr/ark:/12148/cb12519986q#about',
                    'http://data.bnf.fr/ark:/12148/cb12519986q#foaf:Person',
                    'http://dbpedia.org/resource/Bell_hooks',
                    'http://de.dbpedia.org/resource/Bell_hooks',
                    'http://el.dbpedia.org/resource/Μπελλ_Χουκς',
                    'http://es.dbpedia.org/resource/Bell_hooks',
                    'http://fr.dbpedia.org/resource/Bell_hooks',
                    'http://id.dbpedia.org/resource/Bell_hooks',
                    'http://ja.dbpedia.org/resource/ベル・フックス',
                    'http://ko.dbpedia.org/resource/벨_훅스',
                    'http://pl.dbpedia.org/resource/Bell_hooks',
                    'http://pt.dbpedia.org/resource/Bell_hooks',
                    'http://rdf.freebase.com/ns/m.01cj42',
                    'http://ru.dbpedia.org/resource/Белл_хукс',
                    'http://sr.dbpedia.org/resource/Bell_hooks',
                    'http://sv.dbpedia.org/resource/Bell_hooks',
                    'http://tr.dbpedia.org/resource/Bell_hooks',
                    'http://viaf.org/viaf/79115934',
                    'http://wikidata.dbpedia.org/resource/Q259507',
                    'http://www.idref.fr/03444453X/id',
                    'http://www.viaf.org/viaf/79115934',
                    'http://www.wikidata.org/entity/Q259507',
                    'http://yago-knowledge.org/resource/Bell_hooks'},
     'p:BnF_ID_(P268)': 'http://www.wikidata.org/entity/statement/q259507-AAD7573C-ED86-4996-BC7B-AAA3ED7F279B',
     'p:Catalogus_Professorum_Academiae_Rheno-Traiectinae_ID_(P2862)': 'http://www.wikidata.org/entity/statement/Q259507-93DAD149-2259-47D8-8222-01505EB9FD89',
     'p:Commons_category_(P373)': 'http://www.wikidata.org/entity/statement/q259507-13CF0499-B1DA-4E0A-B39F-3AE2C8A91A7E',
     'p:Encyclopædia_Britannica_Online_ID_(P1417)': 'http://www.wikidata.org/entity/statement/Q259507-D2577132-65FF-443F-98C9-CF3A08336295',
     'p:FAST_ID_(P2163)': 'http://www.wikidata.org/entity/statement/Q259507-A34158D9-2D99-4B4E-B3FA-AD4D395C4C8B',
     'p:Freebase_ID_(P646)': 'http://www.wikidata.org/entity/statement/Q259507-FD14E07D-E50A-42C4-A070-0A4E29C5771E',
     'p:GND_ID_(P227)': 'http://www.wikidata.org/entity/statement/q259507-715312D8-B000-416F-9447-F680CD9158BD',
     'p:IMDb_ID_(P345)': 'http://www.wikidata.org/entity/statement/q259507-4D668656-240D-469E-9DA9-495E0B6B20E1',
     'p:ISNI_(P213)': 'http://www.wikidata.org/entity/statement/q259507-71CFAA6B-0A1B-426D-B52A-3E024028BA07',
     'p:Library_of_Congress_authority_ID_(P244)': 'http://www.wikidata.org/entity/statement/q259507-B269132A-E7B4-47A2-BC6D-733C36EC4AE5',
     'p:NDL_Auth_ID_(P349)': 'http://www.wikidata.org/entity/statement/q259507-9EBB3558-8E72-4810-975C-83B02A7ED431',
     'p:NNDB_people_ID_(P1263)': 'http://www.wikidata.org/entity/statement/Q259507-2D7B006E-EF30-4EBD-9B58-3A2665B41F06',
     'p:National_Thesaurus_for_Author_Names_ID_(P1006)': 'http://www.wikidata.org/entity/statement/Q259507-2D16C2BF-746A-4CCE-9A50-951CB67F2663',
     'p:Open_Library_ID_(P648)': 'http://www.wikidata.org/entity/statement/Q259507-5AD28C6A-357F-4743-822D-0C6D50B8D986',
     'p:SELIBR_(P906)': 'http://www.wikidata.org/entity/statement/Q259507-C5C56E5C-BEAC-4503-8802-253F3CF6B143',
     'p:SNAC_Ark_ID_(P3430)': 'http://www.wikidata.org/entity/statement/Q259507-3DAB8303-DEEF-4A26-A7C5-750F5DEE9F81',
     'p:SUDOC_authorities_(P269)': 'http://www.wikidata.org/entity/statement/q259507-A1161925-3A4A-4D52-948C-E5E3DECF6BEC',
     'p:Twitter_username_(P2002)': 'http://www.wikidata.org/entity/statement/Q259507-81383ebb-47e5-368b-a07f-9538f234e9d9',
     'p:University_of_Barcelona_authority_ID_(P1580)': 'http://www.wikidata.org/entity/statement/Q259507-3142EE33-1A76-4B75-8BBF-418F4C76DB1C',
     'p:VIAF_ID_(P214)': 'http://www.wikidata.org/entity/statement/q259507-0EFFD3F2-015E-4586-AE4B-38AD30B8A91C',
     'p:academic_degree_(P512)': 'http://www.wikidata.org/entity/statement/Q259507-B17D6AEB-79CD-43D7-A4EA-60DD7F2B1287',
     'p:award_received_(P166)': 'http://www.wikidata.org/entity/statement/Q259507-7A028CDE-3F3F-4AFB-8E32-61B5CACCCAB5',
     'p:birth_name_(P1477)': 'http://www.wikidata.org/entity/statement/Q259507-0da659a8-4635-4702-d16f-1bc31921b8c3',
     'p:country_of_citizenship_(P27)': 'http://www.wikidata.org/entity/statement/q259507-F3A49353-2B0B-46F7-88E6-3A22B9970FD1',
     'p:date_of_birth_(P569)': 'http://www.wikidata.org/entity/statement/q259507-7E1427B3-29E0-4964-85B0-19B635FB2DD7',
     'p:educated_at_(P69)': {'http://www.wikidata.org/entity/statement/Q259507-DC7D1543-EE13-4CE0-85E0-DDD98C52FC77',
                             'http://www.wikidata.org/entity/statement/Q259507-EABF71A9-74E7-4530-9B64-8C9C66BAE0FE',
                             'http://www.wikidata.org/entity/statement/Q259507-c3e258de-4ed1-7957-ae75-bd7bb78bb9f4'},
     'p:employer_(P108)': {'http://www.wikidata.org/entity/statement/Q259507-0A1D0DED-A570-49E9-986B-137AC041E8D5',
                           'http://www.wikidata.org/entity/statement/Q259507-19B47E59-9229-49B1-B561-B6C9FB53EE4F',
                           'http://www.wikidata.org/entity/statement/Q259507-BD630510-D071-4B8C-AE6A-4724E2EDC902',
                           'http://www.wikidata.org/entity/statement/Q259507-DA4A23BA-C557-4B8F-90C8-8B1DF1397CF9',
                           'http://www.wikidata.org/entity/statement/Q259507-ecfbe4ec-44aa-ccb8-15d7-86cadfe3f29e',
                           'http://www.wikidata.org/entity/statement/Q259507-f2a366a2-4928-1143-eb56-3a1316eab901'},
     'p:ethnic_group_(P172)': 'http://www.wikidata.org/entity/statement/Q259507-4560709D-F5E4-4B51-97C3-F4C731E8F4F4',
     'p:family_name_(P734)': 'http://www.wikidata.org/entity/statement/Q259507-923CDE40-2D69-4285-A9B3-9DB29DD834EA',
     'p:given_name_(P735)': {'http://www.wikidata.org/entity/statement/Q259507-C51AF33D-C3E2-46D8-B913-6E4053E05431',
                             'http://www.wikidata.org/entity/statement/Q259507-ED6CFBB3-806B-4D1F-82AE-5B0871E0D519'},
     'p:image_(P18)': 'http://www.wikidata.org/entity/statement/Q259507-C80387B1-8A7B-4AE7-8722-9E7AA4EFFDCA',
     'p:influenced_by_(P737)': {'http://www.wikidata.org/entity/statement/Q259507-0e0a8624-47a6-fe5d-fade-8f6fdc173989',
                                'http://www.wikidata.org/entity/statement/Q259507-1bf53c1f-4bf8-56a4-2002-cfa49a738844',
                                'http://www.wikidata.org/entity/statement/Q259507-2b4cf37a-430f-65e9-6e99-4c2adca58ca6',
                                'http://www.wikidata.org/entity/statement/Q259507-6597a5c7-41a2-99b0-eefe-32171f1279f1',
                                'http://www.wikidata.org/entity/statement/Q259507-b03e739f-4770-4c8f-cb3c-bb220a855016',
                                'http://www.wikidata.org/entity/statement/Q259507-b36a4f69-4a64-1030-8bb2-ef13a5083bce',
                                'http://www.wikidata.org/entity/statement/Q259507-dc9981dd-49b2-dd18-bce6-f1e49dc7494f',
                                'http://www.wikidata.org/entity/statement/Q259507-dcf5ab55-468e-91d2-fda4-3735ea3d5e02',
                                'http://www.wikidata.org/entity/statement/Q259507-ef6a5c3a-41ff-5c8d-5480-fd7b8ad9ba6d'},
     'p:instance_of_(P31)': 'http://www.wikidata.org/entity/statement/Q259507-84260C80-8984-405C-95BD-36E46D86D549',
     'p:languages_spoken,_written_or_signed_(P1412)': 'http://www.wikidata.org/entity/statement/Q259507-CE3F1503-525C-4052-8039-69A57BD68C3F',
     'p:notable_work_(P800)': {'http://www.wikidata.org/entity/statement/Q259507-0D0487AE-F5CB-4351-9129-E8C8B60C3960',
                               'http://www.wikidata.org/entity/statement/Q259507-258906c9-41f8-d631-3af0-853fb74d7027',
                               'http://www.wikidata.org/entity/statement/Q259507-868E86E6-F421-4550-8CA7-6D1A562DB916',
                               'http://www.wikidata.org/entity/statement/Q259507-B7588702-7C7D-439A-BA8B-973052AF7866',
                               'http://www.wikidata.org/entity/statement/Q259507-C9C8945B-3B08-472A-B8C7-BC057704B5C2'},
     'p:occupation_(P106)': {'http://www.wikidata.org/entity/statement/Q259507-4E2587ED-21C0-4671-A565-DA70A8E2E598',
                             'http://www.wikidata.org/entity/statement/Q259507-7F1A3B03-E55F-47C7-A815-775DFBCAC858'},
     'p:place_of_birth_(P19)': 'http://www.wikidata.org/entity/statement/Q259507-28069175-BAEF-4249-ABC9-9D88E3B9958E',
     'p:sex_or_gender_(P21)': 'http://www.wikidata.org/entity/statement/q259507-F594BDAC-665D-4490-B5BC-0FE5079BE6C7',
     'prop_fr:bnf': {'12519986'},
     'prop_fr:dateDeNaissance': {'1952-09-25+02:00'},
     'prop_fr:famille': {'Mère : Rosa Bell Watkins _(@fr)',
                         'Père : Veodis Watkins _(@fr)'},
     'prop_fr:fr': {'Jamie Glazov _(@fr)'},
     'prop_fr:lang': {'en _(@fr)'},
     'prop_fr:lieuDeNaissance': {'http://fr.dbpedia.org/resource/Hopkinsville',
                                 'http://fr.dbpedia.org/resource/États-Unis'},
     'prop_fr:légende': {'bell hooks en novembre 2009 _(@fr)'},
     'prop_fr:nom': {'bell hooks _(@fr)'},
     'prop_fr:nomDeNaissance': {'Gloria Jean Watkins _(@fr)'},
     'prop_fr:profession': {'intellectuelle et militante féministe _(@fr)'},
     'prop_fr:sudoc': {'3444453'},
     'prop_fr:surnom': {'bell hooks _(@fr)'},
     'prop_fr:texte': {'Jamie Glazov _(@fr)'},
     'prop_fr:trad': {'Jamie Glazov _(@fr)'},
     'prop_fr:type': {'personne _(@fr)'},
     'prop_fr:viaf': {'79115934'},
     'prop_fr:worldcatid': {'lccn-n-82-203435 _(@fr)'},
     'prov:wasDerivedFrom': {'http://en.wikipedia.org/wiki/Bell_hooks?oldid=744683497',
                             'http://fr.wikipedia.org/wiki/Bell_hooks?oldid=106632265'},
     'rdagroup2elements:countryAssociatedWithThePerson': {'http://id.loc.gov/vocabulary/countries/xxu'},
     'rdagroup2elements:fieldOfActivityOfThePerson': {'Sciences sociales. '
                                                      'Sociologie',
                                                      'http://dewey.info/class/300/'},
     'rdfs:comment': {'Bell Hooks (lahir dengan nama Gloria Jean Watkins 25 '
                      'September 1952; umur 61 tahun) adalah seorang intelektual, '
                      'feminis, dan aktivis masyarakat Amerika. hooks memusatkan '
                      'perhatiannya pada kesalingterkaitan antara ras, kelas, dan '
                      'gender dan kemampuan ketiganya itu untuk memproduksi dan '
                      'melestarikan sistem-sistem penindasan dan dominasi. _(@id)',
                      'Gloria Jean Watkins (25 de septiembre de 1952 (64 años) '
                      'Hopkinsville, Kentucky, Estados Unidos) conocida como bell '
                      'hooks (escrito en minúsculas) es una prolífica escritora y '
                      'activista feminista. _(@es)',
                      'Gloria Jean Watkins (Hopkinsville, 25 de setembro de 1952), '
                      'mais conhecida pelo pseudônimo bell hooks (escrito em '
                      'minúsculas), é uma autora, feminista e ativista social '
                      'estadunidense. Watkins tirou o nome "bell hooks" de sua '
                      'bisavó materna, Bell Blair Hooks. Sua escrita tem incidido '
                      'sobre a interconectividade de raça, capitalismo e sexo, que '
                      'ela descreve por sua capacidade de produzir e perpetuar os '
                      'sistemas de opressão e dominação de classe. Ela publicou '
                      'mais de trinta livros e numerosos artigos acadêmicos, '
                      'apareceu em vários filmes e documentários e participou de '
                      'várias palestras públicas. Principalmente através de uma '
                      'perspectiva pós-moderna, hooks aborda raça, classe e gênero '
                      'na educação, arte, história, sexualidade, mídia de massa e '
                      'feminismo. _(@pt)',
                      'Gloria Jean Watkins (born September 25, 1952), better known '
                      'by her pen name bell hooks, is an American author, '
                      'feminist, and social activist. She took her nom de plume '
                      'from her maternal great-grandmother Bell Blair Hooks.Her '
                      'writing has focused on the interconnectivity of race, '
                      'capitalism, and gender and what she describes as their '
                      'ability to produce and perpetuate systems of oppression and '
                      'class domination. _(@en)',
                      'Gloria Jean Watkins (born September 25, 1952), better known '
                      'by her pen name bell hooks, is an American author, '
                      'feminist, and social activist. The name "bell hooks" is '
                      'derived from that of her maternal great-grandmother, Bell '
                      'Blair Hooks. In 2014, she founded the bell hooks Institute '
                      'at Berea College in Berea, Kentucky. _(@en)',
                      'Gloria Jean Watkins, connue sous son nom de plume bell '
                      'hooks, née le 25 septembre 1952, est une intellectuelle, '
                      "féministe, et militante des États-Unis. Elle s'intéresse "
                      'particulièrement aux relations existantes entre race, '
                      'classe et genre, et sur la production et la perpétuation '
                      "des systèmes d'oppression et de domination se basant sur "
                      'eux. Elle a publié plus de trente livres et plusieurs '
                      'articles dans des publications universitaires ou dans la '
                      'presse généraliste, elle est apparue dans plusieurs films '
                      'documentaires, et a participé à des conférences publiques. '
                      "Principalement à partir d'une perspective féministe et "
                      'afro-américaine, hooks traite de la race, de la classe et '
                      "du genre dans l'éducation, l'art, l'histoire, la sexualité, "
                      'les médias de masse, et le féminisme. _(@fr)',
                      'Gloria Jean Watkins, connue sous son nom de plume bell '
                      'hooks, née le 25 septembre 1952, est une intellectuelle, '
                      "féministe, et militante des États-Unis. Elle s'intéresse "
                      'particulièrement aux relations existantes entre race, '
                      'classe et genre, et sur la production et la perpétuation '
                      "des systèmes d'oppression et de domination se basant sur "
                      'eux. _(@fr)',
                      'bell hooks (* 25. September 1952 als Gloria Watkins in '
                      'Hopkinsville, Kentucky) ist eine afroamerikanische '
                      'Literaturwissenschaftlerin und Verfechterin feministischer '
                      'und antirassistischer Ansätze. Ihr Pseudonym ist der Name '
                      'ihrer indigenen Großmutter, den sie aber in Kleinschreibung '
                      'publiziert. _(@de)',
                      'bell hooks, właśc. Gloria Jean Watkins (ur. 25 września '
                      '1952 w Hopkinsville w stanie Kentucky) - amerykańska '
                      'pisarka, poetka, feministka "trzeciej fali". Jedna z '
                      'czołowych przedstawicielek czarnego feminizmu. Autorka '
                      'ponad trzydziestu książek. Edukację rozpoczęła w szkołach '
                      'podlegających segregacji rasowej, przeżyła epokę '
                      'desegregacji. Studiowała na Uniwersytecie Stanforda oraz '
                      'Uniwersytecie Wisconsin-Madison. W roku 1983 obroniła '
                      'doktorat poświęcony Toni Morrison na Uniwersytecie '
                      'Kalifornijskim w Santa Cruz. Wykładała na kilkunastu '
                      'uniwersytetach w USA. _(@pl)',
                      'bell hooks, właśc. Gloria Jean Watkins (ur. 25 września '
                      '1952 w Hopkinsville w stanie Kentucky) - amerykańska '
                      'pisarka, poetka, feministka "trzeciej fali". Jedna z '
                      'czołowych przedstawicielek czarnego feminizmu. Autorka '
                      'ponad trzydziestu książek.Edukację rozpoczęła w szkołach '
                      'podlegających segregacji rasowej, przeżyła epokę '
                      'desegregacji. Studiowała na Uniwersytecie Stanforda oraz '
                      'Uniwersytecie Wisconsin-Madison. _(@pl)',
                      'Глория Джинн Уоткинс (англ. Gloria Jean Watkins), известная '
                      'под псевдонимом белл хукс (англ. bell hooks; род. 25 '
                      'сентября 1952 года) — американская писательница, феминистка '
                      'и социальная активистка. Родилась в 1952 году, семья '
                      'принадлежала к рабочему классу, училась в школе для '
                      'чёрнокожих. Окончила Стэнфордский университет, магистратуру '
                      'прошла в Висконсинском университете в Мадисоне. В 1983 '
                      'получила докторскую степень по литературе, защитив '
                      'диссертацию по творчеству Тони Моррисон. За семь лет до '
                      'этого, работая учительницей, она выпустила свой первый '
                      'сборник стихотворений, впервые используя псевдоним белл '
                      'хукс (позаимствованный ею у прапрабабушки Белл Блэр Хукс). '
                      'Первая публицистическая работа белл хукс, «Разве я не '
                      "женщина?» (Ain't I a Woman?), увидела свет в 1981 году. "
                      '_(@ru)',
                      'جلوريا جينز واتكينز (من مواليد 25 سبتمبر 1952)، المعروفة '
                      'بالاسم المستعار بيل هوكس، هي كاتبة، نسوية، وناشطة '
                      'اجتماعيةأمريكية. اسم "بيل هوكس" مشتق من أن لها جدة رائعة '
                      'تسمى، بيل بلير هوكس. قد ركزت بيل على كتابة في موضوعات '
                      'السنانير حول تقاطع العرق، والرأسمالية، والمساواة بين '
                      'الجنسين، وما وصفته قدرتها على إنتاج وإدامة أنظمة القمع '
                      'والهيمنة الطبقية. وقد نشرت أكثر من 30 كتاب والعديد من '
                      'المقالات العلمية، وظهرت في أفلام وثائقية، وشاركت في '
                      'المحاضرات العامة. في المقام الأول من خلال منظور ما بعد '
                      'الحداثة، وقالت انها عالجت العرقية، والطبقية، والمساواة بين '
                      'الجنسين في التعليم، والفن، والتاريخ، والحياة الجنسية، وسائل '
                      'الإعلام، والنسوية. _(@ar)',
                      'ベル・フックス（bell hooks、本名：Gloria Jean Watkins、1952年9月25日 - '
                      '）は、アフリカ系アメリカ人の知識人であり社会活動家、フェミニストでもある女性である。現在、ニューヨーク市立大学シティカレッジ教授。 '
                      'フックスは、人種、階級、ジェンダーの相互関連性、及びそれらが抑圧と支配のシステムをつくりだし、永続化させてしまう力を持っているということに焦点を当てて研究している。30冊以上のメリカでのノーマライゼーションは白人とアフリカ系アメリカ人の対等の権利や機会のこと）に関する記事を執筆している。また、数本のドキュメンタリー映画に出演し、多くの講演も行っている。黒人女性という観点を基底としながら、教育、芸術、歴史、セクシャリティ、マスメディア、フェミニズム等における人種、社会的階層、ジェンダー問題に取り組んでいる。 '
                      '_(@ja)',
                      'ベル・フックス（bell hooks、本名：Gloria Jean Watkins、1952年9月25日 - '
                      '）は、アフリカ系アメリカ人の知識人であり社会活動家、フェミニストでもある女性である。現在、ニューヨーク市立大学シティカレッジ教授。フックスは、人種、階級、ジェンダーの相互関連ム（mainstream、障害者にも健常者と同じ生活や暮らしのリズムをと訴えるノーマライゼーションのアメリカでの呼び名。ちなみにアメリカでのノーマライゼーションは白人とアフリカ系アメリカ人の対等の権利や機いる。黒人女性という観点を基底としながら、教育、芸術、歴史、セクシャリティ、マスメディア、フェミニズム等における人種、社会的階層、ジェンダー問題に取り組んでいる。 '
                      '_(@ja)'},
     'rdfs:label': {'Bell Hooks _(@de)',
                    'Bell Hooks _(@tr)',
                    'Bell hooks _(@ca)',
                    'Bell hooks _(@de)',
                    'Bell hooks _(@en)',
                    'Bell hooks _(@eo)',
                    'Bell hooks _(@es)',
                    'Bell hooks _(@fi)',
                    'Bell hooks _(@fr)',
                    'Bell hooks _(@hu)',
                    'Bell hooks _(@id)',
                    'Bell hooks _(@nl)',
                    'Bell hooks _(@pl)',
                    'Bell hooks _(@pt)',
                    'Bell hooks _(@sh)',
                    'Bell hooks _(@sr)',
                    'Bell hooks _(@sv)',
                    'Bell hooks _(@tr)',
                    'bell hooks _(@da)',
                    'bell hooks _(@de)',
                    'bell hooks _(@en)',
                    'bell hooks _(@es)',
                    'bell hooks _(@fr)',
                    'bell hooks _(@it)',
                    'bell hooks _(@nb)',
                    'bell hooks _(@nn)',
                    'bell hooks _(@pt)',
                    'bell hooks _(@sl)',
                    'Μπελλ χουκς _(@el)',
                    'Белл хукс _(@ru)',
                    'בל הוקס _(@he)',
                    'بل هوکس _(@fa)',
                    'بيل هوكس _(@ar)',
                    'बेल हुक्स _(@hi)',
                    'ਬੈਲ ਹੁਕਸ _(@pa)',
                    'பெல் ஹூக்சு _(@ta)',
                    'ബെൽ ഹുക്\u200cസ് _(@ml)',
                    'ベル・フックス _(@ja)',
                    '貝爾‧胡克斯 _(@zh)',
                    '벨 훅스 _(@ko)'},

      [...]
    }



.. image:: ../../illustration_delimitante.png
  :width: 600
  :alt: ⚓



Accessing information
----------------------

Raw information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As we have already It is possible to access raw information by simply looking
into the ``attributes`` dictionary::

    bell_hooks.attributes

This dictionary contains all the information retrieved, so it may be quite noisy.


Via keyword search
^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to search a keyword in the result set keys using the function
``get_attributes_with_keyword(keyword)``::

    bell_hooks.get_attributes_with_keyword(u'work')


This gives us a subset of results whose keys match the substring ``work``::

    {
        p:notable_work_(P800): ([ "http://www.wikidata.org/entity/statement/Q259507-C9C8945B-3B08-472A-B8C7-BC057704B5C2","http://www.wikidata.org/entity/statement/Q259507-868E86E6-F421-4550-8CA7-6D1A562DB916","http://www.wikidata.org/entity/statement/Q259507-258906c9-41f8-d631-3af0-853fb74d7027","http://www.wikidata.org/entity/statement/Q259507-0D0487AE-F5CB-4351-9129-E8C8B60C3960","http://www.wikidata.org/entity/statement/Q259507-B7588702-7C7D-439A-BA8B-973052AF7866" ]),
        wdt:notable_work_(P800): ([ "http://www.wikidata.org/entity/Q4697221","http://www.wikidata.org/entity/Q5442867","http://www.wikidata.org/entity/Q4728504","http://www.wikidata.org/entity/Q4941491","http://www.wikidata.org/entity/Q7977716" ])
    }

This feature can also be useful when looking at predicates using the same SPARQL prefix:

>>> bell_hooks.get_attributes_with_keyword(u'foaf:')
{
    'foaf:depiction': {'http://commons.wikimedia.org/wiki/Special:FilePath/Bell_hooks,_October_2014.jpg',
                       'http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg',
                       'http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg?width=300',
                       'https://upload.wikimedia.org/wikipedia/commons/7/7b/Bellhooks.jpg'},
    'foaf:familyName': {'hooks'},
    'foaf:gender': {'female', 'female _(@en)'},
    'foaf:givenName': {'bell'},
    'foaf:isPrimaryTopicOf': {'http://en.wikipedia.org/wiki/Bell_hooks',
                              'http://fr.wikipedia.org/wiki/Bell_hooks'},
    'foaf:name': {'bell hooks', 'bell hooks _(@fr)', 'bell hooks _(@en)'},
    'foaf:nick': {'bell hooks _(@fr)'},
    'foaf:page': {'http://data.bnf.fr/12519986/bell_hooks/'}
}

The literals are all postfixed with their language code.
If you are looking for the labels of an entity in a given language, you can use the labels_by_languages
 class variable:

>>> bell_hooks.labels_by_languages
{
    'ar': ['بيل هوكس'],
     'ca': ['Bell hooks'],
     'da': ['bell hooks'],
     'de': ['bell hooks',
            'Bell hooks',
            'Bell Hooks',
            'Bell Hooks',
            'Gloria Watkins'],
     'el': ['Μπελλ χουκς'],
     'en': ['bell hooks',
            'hooks',
            'bell',
            'bell hooks',
            'bell hooks',
            'hooks',
            'bell',
            'Bell hooks',
            'bell hooks',
            'Gloria Jean Watkins',
            'Gloria Jean Watkins',
            'http://www.wikidata.org/entity/Q4160311',
            'http://www.wikidata.org/entity/Q734575',
            'http://www.wikidata.org/entity/Q17034171',
            'http://www.wikidata.org/entity/statement/Q259507-923CDE40-2D69-4285-A9B3-9DB29DD834EA',
            'http://www.wikidata.org/entity/statement/Q259507-ED6CFBB3-806B-4D1F-82AE-5B0871E0D519',
            'http://www.wikidata.org/entity/statement/Q259507-C51AF33D-C3E2-46D8-B913-6E4053E05431',
            'http://www.wikidata.org/entity/statement/Q259507-2D16C2BF-746A-4CCE-9A50-951CB67F2663',
            'http://www.wikidata.org/entity/statement/Q259507-0da659a8-4635-4702-d16f-1bc31921b8c3',
            'http://www.wikidata.org/entity/statement/Q259507-81383ebb-47e5-368b-a07f-9538f234e9d9',
            '071042342',
            'bellhooks',
            'Gloria Jean Watkins',
            'http://data.bibliotheken.nl/id/thes/p071042342'],
     'eo': ['Bell hooks'],
     'es': ['bell hooks', 'Bell hooks', 'Gloria Jean Watkins'],
     'fa': ['بل هوکس'],
     'fi': ['Bell hooks'],
     'fr': ['bell hooks',
            'bell hooks',
            'Bell hooks',
            'Gloria Jean Watkins',
            'Gloria Jean Watkins'],
     'he': ['בל הוקס'],
     'hi': ['बेल हुक्स'],
     'hu': ['Bell hooks'],
     'id': ['Bell hooks'],
     'it': ['bell hooks', 'Gloria Jean Watkins'],
     'ja': ['ベル・フックス'],
     'ko': ['벨 훅스'],
     'ml': ['ബെൽ ഹുക്\u200cസ്'],
     'nb': ['bell hooks'],
     'nl': ['Bell hooks'],
     'nn': ['bell hooks'],
     'pa': ['ਬੈਲ ਹੁਕਸ'],
     'pl': ['Bell hooks'],
     'pt': ['bell hooks', 'Bell hooks'],
     'ru': ['Белл хукс'],
     'sh': ['Bell hooks', 'Bel huks'],
     'sl': ['bell hooks'],
     'sr': ['Bell hooks'],
     'sv': ['Bell hooks', 'Hooks'],
     'ta': ['பெல் ஹூக்சு'],
     'tr': ['Bell hooks', 'Bell Hooks'],
     'zh': ['貝爾‧胡克斯', '貝爾．胡克斯']
}


Via dedicated methods
^^^^^^^^^^^^^^^^^^^^^^^^


Names
"""""""""

>>> bell_hooks.get_names()
{
   'dbo:birthName': ['Gloria Jean Watkins _(@en)', 'Gloria Jean Watkins _(@fr)'],
    'foaf:familyName': 'hooks',
    'foaf:givenName': 'bell',
    'foaf:name': ['bell hooks', 'bell hooks _(@en)', 'bell hooks _(@fr)'],
    'foaf:nick': 'bell hooks _(@fr)',
    'rdfs:label': ['Bell hooks _(@ca)',
                   'Bell hooks _(@tr)',
                   'ਬੈਲ ਹੁਕਸ _(@pa)',
                   'Белл хукс _(@ru)',
                   'bell hooks _(@de)',
                   'Bell hooks _(@nl)',
                   'bell hooks _(@es)',
                   'בל הוקס _(@he)',
                   'Bell hooks _(@hu)',
                   'Bell hooks _(@fi)',
                   'ബെൽ ഹുക്\u200cസ് _(@ml)',
                   'Μπελλ χουκς _(@el)',
                   'Bell hooks _(@en)',
                   'Bell hooks _(@id)',
                   'bell hooks _(@en)',
                   'bell hooks _(@fr)',
                   'Bell hooks _(@pl)',
                   'bell hooks _(@nn)',
                   'bell hooks _(@pt)',
                   'Bell Hooks _(@tr)',
                   'ベル・フックス _(@ja)',
                   'bell hooks _(@da)',
                   'Bell hooks _(@sv)',
                   'Bell hooks _(@pt)',
                   '벨 훅스 _(@ko)',
                   'bell hooks _(@it)',
                   'Bell hooks _(@de)',
                   'Bell hooks _(@eo)',
                   '貝爾‧胡克斯 _(@zh)',
                   'bell hooks _(@sl)',
                   'Bell hooks _(@sr)',
                   'bell hooks _(@nb)',
                   'Bell hooks _(@fr)',
                   'بل هوکس _(@fa)',
                   'बेल हुक्स _(@hi)',
                   'Bell hooks _(@sh)',
                   'بيل هوكس _(@ar)',
                   'Bell hooks _(@es)',
                   'Bell Hooks _(@de)',
                   'பெல் ஹூக்சு _(@ta)'],
    'skos:altLabel': ['Gloria Jean Watkins _(@it)',
                      'Hooks _(@sv)',
                      'Gloria Jean Watkins _(@fr)',
                      'Bel huks _(@sh)',
                      'Gloria Jean Watkins _(@en)',
                      'Bell Hooks _(@de)',
                      'Gloria Watkins _(@de)',
                      'Gloria Jean Watkins _(@es)',
                      '貝爾．胡克斯 _(@zh)'],
    'wdt:Twitter_username_(P2002)': 'bellhooks',
    'wdt:birth_name_(P1477)': 'Gloria Jean Watkins _(@en)',
    'wdt:family_name_(P734)': 'http://www.wikidata.org/entity/Q17034171',
    'wdt:given_name_(P735)': ['http://www.wikidata.org/entity/Q4160311',
                              'http://www.wikidata.org/entity/Q734575']
}



External Identifiers
""""""""""""""""""""

>>> bell_hooks.get_external_ids()
{
    Deutschen_Nationalbibliothek: ([ "http://d-nb.info/gnd/11933447X" ]),
    ark: ([ "http://data.bnf.fr/ark:/12148/cb12519986q#foaf:Person" ]),
    idref: ([ "http://www.idref.fr/03444453X/id" ]),
    viaf: ([ "http://viaf.org/viaf/79115934" ]),
    wikidata: ([ "http://www.wikidata.org/entity/Q259507" ]),
}



Birth
""""""""""""""""

>>> bell_hooks.get_birth_info()
{
    'date': datetime.datetime(1952, 9, 25, 0, 0),
    'name': {'Gloria Jean Watkins _(@en)', 'Gloria Jean Watkins _(@fr)'},
    'other': '1952-09-25+02:00',
    'place': {'http://dbpedia.org/resource/Hopkinsville,_Kentucky',
              'http://fr.dbpedia.org/resource/Hopkinsville',
              'http://fr.dbpedia.org/resource/États-Unis',
              'http://www.wikidata.org/entity/Q845461'}
}

Death
""""""

>>> bowie = Person(full_name="David Bowie")
>>> endpoints = [Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf]
>>> bowie.add_query_endpoints(endpoints)
>>> bowie.query()
>>> bowie.get_death_info()
{
    cause/manner: ([ "wd:Q3739104","wd:Q623031","dbpedia:Liver_cancer" ]),
    date: ([ "2016-02-10 00:00:00" ]),
    other: ([ "http://data.bnf.fr/date/2016/" ]),
    place: ([ "wd:Q60","New York (New York, États-Unis)" ]),
}



Gender
""""""
>>> leslie = Person(full_name="Leslie Nielsen")
>>> endpoints = [Endpoint.dbpedia_fr, Endpoint.dbpedia, Endpoint.wikidata, Endpoint.bnf]
>>> leslie.add_query_endpoints(endpoints)
>>> leslie.query()
>>> leslie.get_gender()
'M'

.. image:: ../../illustration_delimitante.png
  :width: 600
  :alt: ⚓



Code Documentation
-------------------

See :doc:`pyneql.ontology`.




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
        bnf_onto:firstYear: ([ 1952 ]),
        foaf:depiction: ([ "http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg","https://upload.wikimedia.org/wikipedia/commons/7/7b/Bellhooks.jpg","http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg?width=300" ]),
        foaf:familyName: ([ "hooks" ]),
        foaf:gender: ([ "female" ]),
        foaf:givenName: ([ "bell" ]),
        foaf:name: ([ "bell hooks" ]),
        foaf:page: ([ "http://data.bnf.fr/12519986/bell_hooks/" ]),
        owl:sameAs: ([ "http://data.bnf.fr/ark:/12148/cb12519986q#about","http://viaf.org/viaf/79115934","dbpedia_fr:Bell_hooks","http://data.bnf.fr/ark:/12148/cb12519986q#foaf:Person" ]),
        rdagroup2elements:biographicalInformation: ([ "Essayiste et enseignante. - Militante féminisme et contre la ségragation raciale. - Fondatrice, en 2014, du bell hooks Institute, Berea College (Ky., États-Unis). - Pseudonyme de Gloria Jean Watkins" ]),
        rdagroup2elements:countryAssociatedWithThePerson: ([ "http://id.loc.gov/vocabulary/countries/xxu" ]),
        rdagroup2elements:fieldOfActivityOfThePerson: ([ "Sciences sociales. Sociologie","http://dewey.info/class/300/" ]),
        rdagroup2elements:languageOfThePerson: ([ "http://id.loc.gov/vocabulary/iso639-2/eng" ]),
        rdf:type: ([ "foaf:Person" ]),
        skos:exactMatch: ([ "http://data.bnf.fr/ark:/12148/cb12519986q#foaf:Person" ]),
        validated: ([ 1 ]),
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
        bnf_onto:firstYear: ([ 1952 ]),
        dbo:birthDate: ([ "1952-09-25+02:00","1952-09-25","1952-9-25" ]),
        dbo:birthName: ([ "Gloria Jean Watkins" ]),
        dbo:birthPlace: ([ "http://fr.dbpedia.org/resource/États-Unis","http://dbpedia.org/resource/Hopkinsville,_Kentucky","http://fr.dbpedia.org/resource/Hopkinsville" ]),
        dbo:birthYear: ([ 1952 ]),
        dbo:bnfId: ([ "12519986q" ]),
        dbo:knownFor: ([ "http://dbpedia.org/resource/Feminism","http://dbpedia.org/resource/Activism" ]),
        dbo:occupation: ([ "http://dbpedia.org/resource/Bell_hooks__1","http://fr.dbpedia.org/resource/Intellectuelle" ]),
        dbo:sudocId: ([ "03444453X" ]),
        dbo:viafId: ([ 79115934 ]),
        dbo:wikiPageID: ([ 200734,1156955 ]),
        dbo:wikiPageLength: ([ 18386 ]),
        dbo:wikiPageOutDegree: ([ 71 ]),
        dbo:wikiPageRevisionID: ([ 744683497,106632265 ]),
        dbpprop:viaf: ([ 79115934 ]),
        dbpprop:voy: ([ "no" ]),
        dbpprop:wikt: ([ "no" ]),
        dcterms:description: ([ "American author, feminist, and social activist" ]),
        dcterms:subject: ([ "http://dbpedia.org/resource/Category:1952_births","http://fr.dbpedia.org/resource/Catégorie:Étudiant_de_l'université_de_Californie_à_Santa_Cruz","http://dbpedia.org/resource/Category:African-American_women_writers","http://dbpedia.org/resource/Category:Living_people","http://dbpedia.org/resource/Category:Writers_from_Kentucky","http://dbpedia.org/resource/Category:Stanford_University_alumni","http://dbpedia.org/resource/Category:American_social_activists","http://dbpedia.org/resource/Category:San_Francisco_State_University_faculty","http://dbpedia.org/resource/Category:Poststructuralists","http://dbpedia.org/resource/Category:Postmodern_feminists","http://dbpedia.org/resource/Category:20th-century_African-American_activists","http://fr.dbpedia.org/resource/Catégorie:Féministe_américaine","http://fr.dbpedia.org/resource/Catégorie:Écrivain_américain_du_XXe_siècle","http://fr.dbpedia.org/resource/Catégorie:Femme_de_lettres_américaine","http://fr.dbpedia.org/resource/Catégorie:Personnalité_de_la_lutte_contre_le_racisme","http://dbpedia.org/resource/Category:African-American_studies_scholars","http://dbpedia.org/resource/Category:African-American_feminists","http://fr.dbpedia.org/resource/Catégorie:Étudiant_de_l'université_Stanford","http://dbpedia.org/resource/Category:African-American_non-fiction_writers","http://dbpedia.org/resource/Category:People_from_Hopkinsville,_Kentucky","http://dbpedia.org/resource/Category:Pseudonymous_writers","http://dbpedia.org/resource/Category:Radical_feminists","http://dbpedia.org/resource/Category:Socialist_feminists","http://dbpedia.org/resource/Category:American_feminist_writers","http://dbpedia.org/resource/Category:Anti-poverty_advocates","http://dbpedia.org/resource/Category:Feminist_studies_scholars","http://dbpedia.org/resource/Category:Critical_theorists","http://dbpedia.org/resource/Category:City_University_of_New_York_faculty","http://dbpedia.org/resource/Category:American_socialists","http://dbpedia.org/resource/Category:Critical_race_theory","http://dbpedia.org/resource/Category:20th-century_American_writers","http://fr.dbpedia.org/resource/Catégorie:Essayiste_américain","http://dbpedia.org/resource/Category:21st-century_African-American_activists","http://dbpedia.org/resource/Category:American_women_activists","http://dbpedia.org/resource/Category:Yale_University_faculty","http://dbpedia.org/resource/Category:American_women_philosophers","http://dbpedia.org/resource/Category:21st-century_women_writers","http://dbpedia.org/resource/Category:Postmodern_writers","http://dbpedia.org/resource/Category:21st-century_American_writers","http://fr.dbpedia.org/resource/Catégorie:Naissance_en_septembre_1952","http://fr.dbpedia.org/resource/Catégorie:Nom_de_plume","http://dbpedia.org/resource/Category:University_of_Southern_California_faculty","http://dbpedia.org/resource/Category:University_of_Wisconsin–Madison_alumni","http://dbpedia.org/resource/Category:American_memoirists","http://dbpedia.org/resource/Category:20th-century_women_writers","http://fr.dbpedia.org/resource/Catégorie:Professeur_à_l'université_Yale","http://dbpedia.org/resource/Category:African-American_philosophers","http://fr.dbpedia.org/resource/Catégorie:Naissance_au_Kentucky","http://dbpedia.org/resource/Category:University_of_California,_Santa_Cruz_alumni","http://fr.dbpedia.org/resource/Catégorie:Écrivain_américain_du_XXIe_siècle" ]),
        foaf:depiction: ([ "http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg","https://upload.wikimedia.org/wikipedia/commons/7/7b/Bellhooks.jpg","http://commons.wikimedia.org/wiki/Special:FilePath/Bell_hooks,_October_2014.jpg","http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg?width=300" ]),
        foaf:familyName: ([ "hooks" ]),
        foaf:gender: ([ "female" ]),
        foaf:givenName: ([ "bell" ]),
        foaf:isPrimaryTopicOf: ([ "http://en.wikipedia.org/wiki/Bell_hooks","http://fr.wikipedia.org/wiki/Bell_hooks" ]),
        foaf:name: ([ "bell hooks" ]),
        foaf:nick: ([ "bell hooks" ]),
        foaf:page: ([ "http://data.bnf.fr/12519986/bell_hooks/" ]),
        http://purl.org/linguistics/gold/hypernym: ([ "http://dbpedia.org/resource/Author" ]),
        http://purl.org/voc/vrank#hasRank: ([ "nodeID://b5705506","nodeID://b27429442" ]),
        http://www.wikidata.org/prop/direct-normalized/BnF_ID_(P268): ([ "http://data.bnf.fr/ark:/12148/cb12519986q" ]),
        http://www.wikidata.org/prop/direct-normalized/FAST_ID_(P2163): ([ "http://id.worldcat.org/fast/1801024" ]),
        http://www.wikidata.org/prop/direct-normalized/Freebase_ID_(P646): ([ "http://g.co/kg/m/01cj42" ]),
        http://www.wikidata.org/prop/direct-normalized/GND_ID_(P227): ([ "http://d-nb.info/gnd/11933447X" ]),
        http://www.wikidata.org/prop/direct-normalized/Library_of_Congress_authority_ID_(P244): ([ "http://id.loc.gov/authorities/names/n82203435" ]),
        d:P800s: ([ "http://www.wikidata.org/entity/Q259507SC9C8945B-3B08-472A-B8C7-BC057704B5C2","http://www.wikidata.org/entity/Q259507SB7588702-7C7D-439A-BA8B-973052AF7866","http://www.wikidata.org/entity/Q259507S868E86E6-F421-4550-8CA7-6D1A562DB916","http://www.wikidata.org/entity/Q259507S0D0487AE-F5CB-4351-9129-E8C8B60C3960" ]),
        wdt:BnF_ID_(P268): ([ "12519986q" ]),
        wdt:Encyclopædia_Britannica_Online_ID_(P1417): ([ "biography/bell-hooks" ]),
        wdt:FAST_ID_(P2163): ([ 1801024 ]),
        wdt:Freebase_ID_(P646): ([ "/m/01cj42" ]),
        wdt:GND_ID_(P227): ([ "11933447X" ]),
        wdt:IMDb_ID_(P345): ([ "nm0393654" ]),
        wdt:ISNI_(P213): ([ "0000 0001 1072 449X" ]),
        wdt:Library_of_Congress_authority_ID_(P244): ([ "n82203435" ]),
        wdt:NDL_Auth_ID_(P349): ([ 00544810 ]),
        wdt:NNDB_people_ID_(P1263): ([ "593/000115248" ]),
        wdt:National_Thesaurus_for_Author_Names_ID_(P1006): ([ 071042342 ]),
        wdt:Open_Library_ID_(P648): ([ "OL2631291A" ]),
        wdt:SELIBR_(P906): ([ 374125 ]),
        wdt:SNAC_Ark_ID_(P3430): ([ "w6rn5sgw" ]),
        wdt:SUDOC_authorities_(P269): ([ "03444453X" ]),
        wdt:Twitter_username_(P2002): ([ "bellhooks" ]),
        wdt:University_of_Barcelona_authority_ID_(P1580): ([ "a1352485" ]),
        wdt:VIAF_ID_(P214): ([ 79115934 ]),
        wdt:academic_degree_(P512): ([ "http://www.wikidata.org/entity/Q849697" ]),
        wdt:award_received_(P166): ([ "http://www.wikidata.org/entity/Q463606" ]),
        wdt:birth_name_(P1477): ([ "Gloria Jean Watkins" ]),
        wdt:country_of_citizenship_(P27): ([ "http://www.wikidata.org/entity/Q30" ]),
        wdt:date_of_birth_(P569): ([ "1952-09-25T00:00:00Z" ]),
        wdt:educated_at_(P69): ([ "http://www.wikidata.org/entity/Q41506","http://www.wikidata.org/entity/Q1047293","http://www.wikidata.org/entity/Q838330" ]),
        wdt:employer_(P108): ([ "http://www.wikidata.org/entity/Q846859","http://www.wikidata.org/entity/Q4614","http://www.wikidata.org/entity/Q1256981","http://www.wikidata.org/entity/Q616591","http://www.wikidata.org/entity/Q49112","http://www.wikidata.org/entity/Q762266" ]),
        wdt:family_name_(P734): ([ "http://www.wikidata.org/entity/Q17034171" ]),
        wdt:given_name_(P735): ([ "http://www.wikidata.org/entity/Q4160311","http://www.wikidata.org/entity/Q734575" ]),
        wdt:influenced_by_(P737): ([ "http://www.wikidata.org/entity/Q273210","http://www.wikidata.org/entity/Q164797","http://www.wikidata.org/entity/Q8027","http://www.wikidata.org/entity/Q461758","http://www.wikidata.org/entity/Q335384","http://www.wikidata.org/entity/Q105180","http://www.wikidata.org/entity/Q57085","http://www.wikidata.org/entity/Q310913","http://www.wikidata.org/entity/Q43303" ]),
        wdt:notable_work_(P800): ([ "http://www.wikidata.org/entity/Q4697221","http://www.wikidata.org/entity/Q5442867","http://www.wikidata.org/entity/Q4728504","http://www.wikidata.org/entity/Q4941491","http://www.wikidata.org/entity/Q7977716" ]),
        wdt:occupation_(P106): ([ "http://www.wikidata.org/entity/Q1622272","http://www.wikidata.org/entity/Q4964182" ]),
        wdt:place_of_birth_(P19): ([ "http://www.wikidata.org/entity/Q845461" ]),
        wdt:sex_or_gender_(P21): ([ "http://www.wikidata.org/entity/Q6581072" ]),

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
    foaf:depiction: ([ "http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg","https://upload.wikimedia.org/wikipedia/commons/7/7b/Bellhooks.jpg","http://commons.wikimedia.org/wiki/Special:FilePath/Bell_hooks,_October_2014.jpg","http://commons.wikimedia.org/wiki/Special:FilePath/Bellhooks.jpg?width=300" ]),
    foaf:familyName: ([ "hooks" ]),
    foaf:gender: ([ "female" ]),
    foaf:givenName: ([ "bell" ]),
    foaf:isPrimaryTopicOf: ([ "http://en.wikipedia.org/wiki/Bell_hooks","http://fr.wikipedia.org/wiki/Bell_hooks" ]),
    foaf:name: ([ "bell hooks" ]),
    foaf:nick: ([ "bell hooks" ]),
    foaf:page: ([ "http://data.bnf.fr/12519986/bell_hooks/" ]),
}

.. note::
    It is not yet possible to filter results by languages. It's on my todo list. Feel free to contribute to the project on `GitHub <https://github.com/Valerie-Hanoka/PyNeQL>`_ !


Via dedicated methods
^^^^^^^^^^^^^^^^^^^^^^^^


Names
"""""""""

>>> bell_hooks.get_names()
{
    dbo:birthName: ([ "Gloria Jean Watkins" ]),
    foaf:familyName: ([ "hooks" ]),
    foaf:givenName: ([ "bell" ]),
    foaf:name: ([ "bell hooks" ]),
    foaf:nick: ([ "bell hooks" ]),
    rdfs:label: ([ "bell hooks","Μπελλ χουκς","بيل هوكس","ベル・フックス","Белл хукс","貝爾‧胡克斯","ਬੈਲ ਹੁਕਸ","بل هوکس","Bell Hooks","בל הוקס","बेल हुक्स","பெல் ஹூக்சு","벨 훅스","Bell hooks","ബെൽ ഹുക്‌സ്" ]),
    skos:altLabel: ([ "Bell Hooks","Gloria Jean Watkins","貝爾．胡克斯","Bel huks","Gloria Watkins","Hooks" ]),
    wdt:Twitter_username_(P2002): ([ "bellhooks" ]),
    wdt:birth_name_(P1477): ([ "Gloria Jean Watkins" ]),
    wdt:family_name_(P734): ([ "http://www.wikidata.org/entity/Q17034171" ]),
    wdt:given_name_(P735): ([ "http://www.wikidata.org/entity/Q4160311","http://www.wikidata.org/entity/Q734575" ]),
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
    date: ([ "1952-09-25 00:00:00" ]),
    name: ([ "Gloria Jean Watkins" ]),
    other: ([ "1952-09-25+02:00" ]),
    place: ([ "http://fr.dbpedia.org/resource/États-Unis","http://dbpedia.org/resource/Hopkinsville,_Kentucky","http://www.wikidata.org/entity/Q845461","http://fr.dbpedia.org/resource/Hopkinsville" ])
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




Thing
=========================================

The class ``Thing`` will only be used as a common parent for all other named entities classes.
As it is not safe to use, I describe it there just for fun.



.. image:: ../../illustration_delimitante.png
  :width: 600
  :alt: ⚓


Looking for *any*-Thing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Basic search
"""""""""""""

We want to find `አዲስ አበባ <https://en.wikipedia.org/wiki/Addis_Ababa>`_ (in Amharic) on DBPedia::

    from pyneql.ontology.thing import Thing
    from pyneql.utils.endpoints import Endpoint
    from pyneql.utils.enum import LanguagesIso6391 as Lang

    # Creating the Thing using its label, the language of the label
    # (If no language is specified, English is used)
    # and the endpoint on which the object should be queried.
    addis_abeba = Thing(
        label=u'አዲስ አበባ',
        query_language=Lang.Amharic,
        endpoints=[Endpoint.dbpedia])

    # Sending the query
    addis_abeba.query()

Once the query is sent, the results are stored in the object's ``attributes`` dictionary.



Extended search
"""""""""""""""""

If the element we are looking for is ubiquitous in the Semantic Web, we may
want to search further. The function ``find_more_about()`` is doing that.
Before the exectution of the function ``find_more_about()``, we have 72 RDF predicates having values for Addis Abeba:


>>> addis_abeba = Thing(label=u'አዲስ አበባ', query_language=Lang.Amharic)
>>> addis_abeba.add_query_endpoints([Endpoint.dbpedia, Endpoint.wikidata])
>>> addis_abeba.query(strict_mode=True, check_type=True)
>>> len(addis_abeba.attributes)
72

Executing the function add some more

>>> addis_abeba.find_more_about()
>>> len(addis_abeba.attributes)
176


This feature just takes the URIs of the first result set which are the objects
of identity predicates (``skos:exactMatch``, ``owl:sameAs``) and retrieve the associated RDF triples.

*N.B.: The numbers of attributes given here for this example are susceptible to variations.*

.. image:: ../../illustration_delimitante.png
  :width: 600
  :alt: ⚓



Accessing information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Raw information
""""""""""""""""

It is possible to access raw information like that::

    addis_abeba.attributes

This dictionary contains all the information retrieved, so it is quite noisy.
For instance here for Addis Abeba, the content is::

    {
        http://purl.org/voc/vrank#hasRank': 'nodeID://b5794744',
        'owl:sameAs': 'wd:Q3624',
        'rdf:type': {'wd:Q1637706', 'wd:Q5119', 'wdt_o:Item'},
        'rdfs:label': {'Adas Ababa _(@ga)',
                       'Addis Ababa _(@cy)',
                       'Addis Ababa _(@da)',
                       'Addis Ababa _(@en)',
                       'Addis Ababa _(@fo)',
                       'Addis Ababa _(@gd)',
                       'Addis Ababa _(@ha)',
                       'Addis Ababa _(@hif)',
                       'Addis Ababa _(@id)',
                       'Addis Ababa _(@ig)',
                       'Addis Ababa _(@io)',
                       'Addis Ababa _(@is)',
                       'Addis Ababa _(@jv)',
                       'Addis Ababa _(@ms)',
                       'Addis Ababa _(@pap)',
                       'Addis Ababa _(@rup)',
                       'Addis Ababa _(@rw)',
                       'Addis Ababa _(@sco)',
                       'Addis Ababa _(@sn)',
                       'Addis Ababa _(@sw)',
                       'Addis Ababa _(@tl)',
                       'Addis Ababa _(@tr)',
                       'Addis Ababa _(@vi)',
                       'Addis Ababa _(@war)',
                       'Addis Ababa _(@yo)',
                       'Addis Abeba _(@af)',
                       'Addis Abeba _(@an)',
                       'Addis Abeba _(@br)',
                       'Addis Abeba _(@ca)',
                       'Addis Abeba _(@cs)',
                       'Addis Abeba _(@de)',
                       'Addis Abeba _(@dsb)',
                       'Addis Abeba _(@et)',
                       'Addis Abeba _(@eu)',
                       'Addis Abeba _(@fi)',
                       'Addis Abeba _(@fy)',
                       'Addis Abeba _(@hsb)',
                       'Addis Abeba _(@ie)',
                       'Addis Abeba _(@it)',
                       'Addis Abeba _(@kaa)',
                       'Addis Abeba _(@kab)',
                       'Addis Abeba _(@lb)',
                       'Addis Abeba _(@lij)',
                       'Addis Abeba _(@lmo)',
                       'Addis Abeba _(@mg)',
                       'Addis Abeba _(@nan)',
                       'Addis Abeba _(@nb)',
                       'Addis Abeba _(@nl)',
                       'Addis Abeba _(@nn)',
                       'Addis Abeba _(@oc)',
                       'Addis Abeba _(@om)',
                       'Addis Abeba _(@pl)',
                       'Addis Abeba _(@pms)',
                       'Addis Abeba _(@rm)',
                       'Addis Abeba _(@ro)',
                       'Addis Abeba _(@sc)',
                       'Addis Abeba _(@sk)',
                       'Addis Abeba _(@so)',
                       'Addis Abeba _(@sq)',
                       'Addis Abeba _(@srn)',
                       'Addis Abeba _(@sv)',
                       'Addis Abeba _(@vec)',
                       'Addis Abeba _(@vro)',
                       'Addis-Abeb _(@vep)',
                       'Addis-Abeba _(@fr)',
                       'Addis-Abeba _(@uz)',
                       'Addis-Abeba _(@wo)',
                       'Addisz-Abeba _(@hu)',
                       'Adis Ababa _(@nov)',
                       'Adis Ababa _(@qu)',
                       'Adis Abeba _(@bs)',
                       'Adis Abeba _(@diq)',
                       'Adis Abeba _(@hr)',
                       'Adis Abeba _(@kg)',
                       'Adis Abeba _(@lt)',
                       'Adis Abeba _(@nah)',
                       'Adis Abeba _(@pt)',
                       'Adis Abeba _(@pt-br)',
                       'Adis Abeba _(@sgs)',
                       'Adis Abeba _(@sh)',
                       'Adis Abeba _(@sl)',
                       'Adis-Abeba _(@ht)',
                       'Adis-Abebo _(@eo)',
                       'Adisabeba _(@lv)',
                       'Adís Abeba _(@es)',
                       'Adís Abeba _(@gl)',
                       'Neanthopolis _(@la)',
                       'Əddis-Əbəbə _(@az)',
                       'Αντίς Αμπέμπα _(@el)',
                       'Аддис-Абебæ _(@os)',
                       'Аддис-Абеба _(@ba)',
                       'Аддис-Абеба _(@ce)',
                       'Аддис-Абеба _(@kk)',
                       'Аддис-Абеба _(@ky)',
                       'Аддис-Абеба _(@mn)',
                       'Аддис-Абеба _(@mrj)',
                       'Аддис-Абеба _(@ru)',
                       'Аддис-Абеба _(@tg)',
                       'Аддис-Абеба _(@udm)',
                       'Аддис-Абеба _(@uk)',
                       'Адис Абеба _(@bg)',
                       'Адис Абеба _(@mk)',
                       'Адис Абеба _(@sr)',
                       'Адыс-Абэба _(@be-tarask)',
                       'Горад Адыс-Абеба _(@be)',
                       'Ադիս Աբեբա _(@hy)',
                       'אדיס אבאבא _(@yi)',
                       'אדיס אבבה _(@he)',
                       'آدیس آبابا _(@fa)',
                       'أديس أبابا _(@ar)',
                       'ئادیس ئابابا _(@ckb)',
                       'اديس ابابا _(@arz)',
                       'ادیس ابابا _(@pnb)',
                       'ادیس ابابا _(@ur)',
                       'अदिस अबाबा _(@mr)',
                       'अदिस अबाबा _(@new)',
                       'अदीस अबाबा _(@hi)',
                       'আদ্দিস আবাবা _(@bn)',
                       'ਆਦਿਸ ਆਬਬਾ _(@pa)',
                       'அடிஸ் அபாபா _(@ta)',
                       'అద్దిస్ అబాబా _(@te)',
                       'ಅಡಿಸ್ ಅಬಾಬ _(@kn)',
                       'അഡിസ് അബെബ _(@ml)',
                       'แอดดิสอาบาบา _(@th)',
                       'ཨ་ཌི་སི་ཨ་བ་བ། _(@bo)',
                       'အာဒစ် အာဘာဘာမြို့ _(@my)',
                       'ადის-აბება _(@ka)',
                       'ადის-აბება _(@xmf)',
                       'አዲስ አበባ _(@am)',
                       'アディスアベバ _(@ja)',
                       '亚的斯亚贝巴 _(@wuu)',
                       '亚的斯亚贝巴 _(@zh)',
                       '亚的斯亚贝巴 _(@zh-hans)',
                       '阿迪斯阿貝巴 _(@yue)',
                       '阿迪斯阿貝巴 _(@zh-hant)',
                       '아디스아바바 _(@ko)'},
        'rdfs:seeAlso': {'http://d-nb.info/gnd/4000459-4/about/rdf',
                         'http://data.bnf.fr/ark:/12148/cb119947834',
                         'http://id.loc.gov/authorities/names/n79061184',
                         'http://musicbrainz.org/8474f16d-03a0-4a09-adf3-df2d1e65ba2f/area',
                         'http://sws.geonames.org/344979/about.rdf',
                         'http://viaf.org/viaf/141880939/rdf.xml'},
        'schema:description': {"Capitale de l'Éthiopie _(@fr)",
                               'Etiopias hovedstad _(@nb)',
                               'Hauptstadt von Äthiopien _(@de)',
                               'capital city of Ethiopia _(@en)',
                               'capital e a maior cidade da Etiópia _(@pt-br)',
                               'capital e cidade máis poboada de Etiopía _(@gl)',
                               'capital y ciudad más poblada de Etiopía _(@es)',
                               "città autonoma e capitale dell'Etiopia _(@it)",
                               'stad in Ethiopië _(@nl)',
                               'πρωτεύουσα της Αιθιοπίας _(@el)',
                               'столица Эфиопии _(@ru)',
                               'בירת אתיופיה _(@he)',
                               'הויפטשטאט פון עטיאפיע _(@yi)',
                               'इथियोपिया और अफ्रीकी संघ की राजधानी और सबसे बड़ा नगर '
                               '_(@hi)',
                               '埃塞俄比亚首都 _(@zh-hans)'},
        'skos:altLabel': {'Addis _(@nb)', 'Āddīs Ābebā _(@gl)', 'Finifinee _(@en)'},
        'skos:exactMatch': 'wd:Q3624',
        'validated': 1,
        'wd:P1296c': '0000693',
        'wd:P1296s': 'wd:Q3624S19F2DC2E-D87D-43F8-93F2-E14091B7227C',
        'wd:P131c': 'wd:Q115',
        'wd:P131s': 'wd:Q3624S1D0A87FC-3366-4834-B6FE-7B477D146C64',
        'wd:P1376c': {'wd:Q115',
                      'wd:Q207521',
                      'wd:Q2603305',
                      'wd:Q328478',
                      'wd:Q940821'},
        'wd:P1376s': {'wd:Q3624S0F815FBF-9880-4E4B-A896-34BA27FBAA25',
                      'wd:Q3624S620F4C91-0794-4862-8064-2397B8BC8152',
                      'wd:Q3624S7A150092-DB8B-4F13-B7B4-3EF71D20F483',
                      'wd:Q3624S7AF2107A-3FA4-44CC-BA4F-89B3D0C3BB76',
                      'wd:Q3624SFA52F9D2-E23F-455D-9DE4-D78254292864'},
        'wd:P1464c': 'wd:Q8042512',
        'wd:P1464s': 'wd:Q3624S34BB5F6F-9F47-4C0E-84E5-2635CB7E666B',
        'wd:P1465c': 'wd:Q9220488',
        'wd:P1465s': 'wd:Q3624S6A273F76-363C-48AE-A1C5-8A89CEABB3FC',
        'wd:P1566c': '344979',
        'wd:P1566s': 'wd:Q3624SE098E58A-752A-4781-A8C0-62D2D2819E81',
        'wd:P1792c': 'wd:Q7905678',
        'wd:P1792s': 'wd:Q3624S69696269-BA7F-48C9-A456-9C0D3D587DB1',
        'wd:P17c': 'wd:Q115',
        'wd:P17s': 'wd:Q3624SA3142BF0-D61C-41DD-95AC-5CA90BB24B22',
        'wd:P18c': {'http://commons.wikimedia.org/wiki/File:Addis_Abeba,_Ethiopia.jpg',
                    'http://commons.wikimedia.org/wiki/File:Addis_Abeba_montage_1.jpg'},
        'wd:P18s': {'wd:Q3624S3A3DFD35-D0ED-4E62-9CE2-C507F32DF1CF',
                    'wd:Q3624SA63AC232-2D53-40BE-B863-29672C2A45C5'},
        'wd:P190c': {'wd:Q11725',
                     'wd:Q1754',
                     'wd:Q192225',
                     'wd:Q1963',
                     'wd:Q2079',
                     'wd:Q33935',
                     'wd:Q34647',
                     'wd:Q4115712',
                     'wd:Q41843',
                     'wd:Q42148',
                     'wd:Q61',
                     'wd:Q62',
                     'wd:Q956'},
        'wd:P190s': {'wd:Q3624S03eb573f-4e91-72f2-715b-737fb5665d30',
                     'wd:Q3624S0bb8fe71-4421-1134-c4e7-15cc9ed6e4e3',
                     'wd:Q3624S439D4620-D88D-4941-A44F-C392994892DA',
                     'wd:Q3624S58430ABE-3409-4CDC-B9E0-A7C9F187996C',
                     'wd:Q3624S5c2c5b70-4ebb-89f2-4e62-a9dbac0ac94b',
                     'wd:Q3624S6242dfad-43d5-5d4e-2b32-cb23b31cac1b',
                     'wd:Q3624SF25F050C-DDA2-49FB-903F-FDAD1D3B0EEE',
                     'wd:Q3624SF7121691-55FD-4674-85BE-DF3046BA5B65',
                     'wd:Q3624SF795AD2C-3AAF-4F1D-9D7F-F56265CE110B',
                     'wd:Q3624Saed04f83-4988-dd20-8049-1038299e8ddb',
                     'wd:Q3624Saf2ff214-45e5-8ac1-6bf8-ed0e7d4a061e',
                     'wd:Q3624Sb9c07dda-4318-43ed-12b2-df6bb5d0af6e',
                     'wd:Q3624Se480f05f-42e2-261a-4c09-d98597a406c8'},
        'wd:P2044c': '2355',
        'wd:P2044s': 'wd:Q3624S6DC89AB6-E1C0-4BAB-9427-5DE12A1B2F4C',
        'wd:P214c': '141880939',
        'wd:P214s': 'wd:Q3624SB25B5577-0C7A-4113-B996-0E55559BEB05',
        'wd:P227c': '4000459-4',
        'wd:P227s': 'wd:Q3624S9F723A38-F075-4705-97A3-5D4CA21921D3',
        'wd:P244c': 'n79061184',
        'wd:P244s': 'wd:Q3624S16E2B954-96FA-4920-9DFA-7449F2937EB0',
        'wd:P268c': '119947834',
        'wd:P268s': 'wd:Q3624SFFC6BCE7-5C51-4D79-BC98-CEE22899B3D1',
        'wd:P300c': 'ET-AA',
        'wd:P300s': 'wd:Q3624SBEEEB449-C42A-4B89-B0C9-75862406B0B7',
        'wd:P31c': {'wd:Q1637706', 'wd:Q5119'},
        'wd:P31s': {'wd:Q3624S30e47a93-439e-4814-1cf6-b8905af9b684',
                    'wd:Q3624Sa67a20f3-4b64-86cc-2495-43342fff7e73'},
        'wd:P373c': 'Addis Ababa',
        'wd:P373s': 'wd:Q3624S826F9B52-12B3-4247-B6D2-44A022F5F3A8',
        'wd:P402c': '1707699',
        'wd:P402s': 'wd:Q3624S84ce2096-48c5-281a-b653-85adb42c8522',
        'wd:P421c': 'wd:Q6760',
        'wd:P421s': 'wd:Q3624S0EA73678-4B48-45B2-9966-853C750786C5',
        'wd:P47c': 'wd:Q202107',
        'wd:P47s': 'wd:Q3624S2B77959C-D191-4C7C-9EF5-37BB6137F53F',
        'wd:P501c': 'wd:Q202107',
        'wd:P501s': 'wd:Q3624S59a9fa46-485a-1ff6-dae3-b1042742d09b',
        'wd:P571c': '1886',
        'wd:P571s': 'wd:Q3624S042796ae-4e14-35b8-8403-5746bfbbe5a7',
        'wd:P625c': 'wd:VCdbe83a5eacb4564dfaa0b9eb374bd627',
        'wd:P625s': 'wd:Q3624S7281893B-562E-4D07-B61A-87B6E7E4B5EE',
        'wd:P646-freebase': 'freebase:m.0dttf',
        'wd:P646c': '/m/0dttf',
        'wd:P646s': 'wd:Q3624S5ADDAF15-6E16-4839-9BF6-344FEB79E162',
        'wd:P691c': 'ge560694',
        'wd:P691s': 'wd:Q3624S5A0C7AB4-C305-4F0E-818C-15F45D796829',
        'wd:P901c': 'ET44',
        'wd:P901s': 'wd:Q3624SCBDA79A9-1335-486A-8004-8FE076D39187',
        'wd:P910c': 'wd:Q6494411',
        'wd:P910s': 'wd:Q3624S70F309C9-D0DB-4C7C-9DAB-00F8646611BD',
        'wd:P935c': 'አዲስ አበባ',
        'wd:P935s': 'wd:Q3624S8304D42A-447E-404E-997C-DCDE7223D681',
        'wd:P948c': 'http://commons.wikimedia.org/wiki/File:Addis_Ababa_banner_Churchill_Avenue.jpg',
        'wd:P948s': 'wd:Q3624SD5575C92-2486-4985-9E74-223A3C53326D',
        'wd:P982c': '8474f16d-03a0-4a09-adf3-df2d1e65ba2f',
        'wd:P982s': 'wd:Q3624S0BFCAE75-E74B-4632-8083-E1880EA1B185'
    }




Via keyword search
""""""""""""""""""""""

It is possible to search a regular expression in the result set keys::

    addis_abeba.get_attributes_with_keyword("rdfs?:")

This gives us a subset of results which keys use `rdf` or `rdfs` prefixes::

    {
        'rdf:type': {'wd:Q5119', 'wd:Q1637706', 'wdt_o:Item'},
        'rdfs:label': {'Adas Ababa _(@ga)',
                       'Addis Ababa _(@cy)',
                       [...]
                       'Аддис-Абеба _(@udm)',
                       'Аддис-Абеба _(@uk)',
                       'Адис Абеба _(@bg)',
                       'Горад Адыс-Абеба _(@be)',
                       'Ադիս Աբեբա _(@hy)',
                       'آدیس آبابا _(@fa)',
                       'ادیس ابابا _(@ur)',
                       'अदिस अबाबा _(@mr)',
                       'अदिस अबाबा _(@new)',
                       'अदीस अबाबा _(@hi)',
                       'আদ্দিস আবাবা _(@bn)',
                       'ਆਦਿਸ ਆਬਬਾ _(@pa)',
                       'அடிஸ் அபாபா _(@ta)',
                       'అద్దిస్ అబాబా _(@te)',
                       'ಅಡಿಸ್ ಅಬಾಬ _(@kn)',
                       'അഡിസ് അബെബ _(@ml)',
                       'แอดดิสอาบาบา _(@th)',
                       'ཨ་ཌི་སི་ཨ་བ་བ། _(@bo)',
                       'အာဒစ် အာဘာဘာမြို့ _(@my)',
                       'ადის-აბება _(@ka)',
                       'ადის-აბება _(@xmf)',
                       'አዲስ አበባ _(@am)',
                       'アディスアベバ _(@ja)',
                       '亚的斯亚贝巴 _(@wuu)',
                       '亚的斯亚贝巴 _(@zh)',
                       '아디스아바바 _(@ko)'},
        'rdfs:seeAlso': {'http://d-nb.info/gnd/4000459-4/about/rdf',
                         'http://data.bnf.fr/ark:/12148/cb119947834',
                         'http://id.loc.gov/authorities/names/n79061184',
                         'http://musicbrainz.org/8474f16d-03a0-4a09-adf3-df2d1e65ba2f/area',
                         'http://sws.geonames.org/344979/about.rdf',
                         'http://viaf.org/viaf/141880939/rdf.xml'}
    }

The literals are all postfixed with their language code.
If you are looking for the labels of an entity in a given language, you can use the `labels_by_languages` class variable:

>>> addis_abeba.labels_by_languages
    {
         'af': ['Addis Abeba'],
         'am': ['አዲስ አበባ'],
         'an': ['Addis Abeba'],
         'ar': ['أديس أبابا'],
         'arz': ['اديس ابابا'],
         'az': ['Əddis-Əbəbə'],
         'ba': ['Аддис-Абеба'],
         'be': ['Горад Адыс-Абеба'],
         'be-tarask': ['Адыс-Абэба'],
         'bg': ['Адис Абеба'],
         'bn': ['আদ্দিস আবাবা'],
         'bo': ['ཨ་ཌི་སི་ཨ་བ་བ།'],
         'br': ['Addis Abeba'],
         'bs': ['Adis Abeba'],
         'ca': ['Addis Abeba'],
         'ce': ['Аддис-Абеба'],
         'ckb': ['ئادیس ئابابا'],
         'cs': ['Addis Abeba'],
         'cy': ['Addis Ababa'],
         'da': ['Addis Ababa'],
         'de': ['Addis Abeba'],
         'diq': ['Adis Abeba'],
         'dsb': ['Addis Abeba'],
         'el': ['Αντίς Αμπέμπα'],
         'en': ['Addis Ababa', 'Finifinee'],
          [...]
    }



.. image:: ../../illustration_delimitante.png
  :width: 600
  :alt: ⚓



Code Documentation
^^^^^^^^^^^^^^^^^^

See :doc:`pyneql.ontology`.




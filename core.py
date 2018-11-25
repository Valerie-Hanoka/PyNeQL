#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka
"""

# Debug:

from pyneql.ontology.thing import Thing
from pyneql.utils.enum import LanguagesIso6391 as Lang
from pyneql.utils.endpoints import Endpoint


from pyneql.query.rdftriple import RDFTriple
from pyneql.query.querybuilder import GenericSPARQLQuery
from pyneql.utils.namespace import NameSpace
from fuzzywuzzy import fuzz

import pprint, ipdb

from pyneql.ontology.person import Person


from pyneql.utils.utils import pretty_print_utf8

from pyneql.ontology.person import Person
from pyneql.ontology.creative_work import CreativeWork
from pyneql.ontology.book import Book
from pyneql.utils.endpoints import Endpoint
from pyneql.utils.enum import LanguagesIso6391 as Lang

from pyneql.ontology.thing import Thing
from pyneql.utils.endpoints import Endpoint
from pyneql.utils.enum import LanguagesIso6391 as Lang

work1 = CreativeWork(
        title="Une chambre à soi",
        author="Virginia Woolf",
        query_language=Lang.French,
        endpoints=[Endpoint.bnf])

work1.query(strict_mode=False, check_type=False)
import pprint; pprint.pprint(work1.attributes)
import ipdb; ipdb.set_trace()

exit()

work3 = CreativeWork(
    title=u"Vieilles Chansons du pays Imerina",
    author=u"Rabearivelo",
    endpoints=[Endpoint.wikidata],
    query_language=Lang.French)

work3.query(strict_mode=False, check_type=True)

print(work3.query_builder.queries.get(Endpoint.wikidata))

#PREFIX schema: <http://schema.org/>
#PREFIX dct: <http://purl.org/dc/terms/>
#PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#SELECT DISTINCT ?CreativeWork ?pred ?obj WHERE {
#  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ja". }
#  ?CreativeWork ?pred ?obj .
#  { ?CreativeWork ?has_author <http://www.wikidata.org/entity/Q5586>  }
#  UNION { ?CreativeWork ?has_author <http://rdf.freebase.com/ns/m.0bwf4>  }
#  UNION { ?CreativeWork ?has_author <http://dbpedia.org/resource/Hokusai>  }
#  UNION { ?CreativeWork ?has_author <http://ja.dbpedia.org/resource/葛飾北斎>  } .
#  { ?CreativeWork schema:alternativeHeadline "凱風快晴"@ja  }
#  UNION { ?CreativeWork foaf:name "凱風快晴"@ja  }
#  UNION { ?CreativeWork schema:alternateName "凱風快晴"@ja  }
#  UNION { ?CreativeWork dct:title "凱風快晴"@ja  }
#  UNION { ?CreativeWork schema:name "凱風快晴"@ja  } .
#} LIMIT 1500


#SELECT DISTINCT ?CreativeWork ?pred ?obj WHERE
#{ SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ja". }
# ?CreativeWork ?has_title "凱風快晴"@ja .
# ?CreativeWork ?pred ?obj .
# { ?CreativeWork ?has_author <http://ja.dbpedia.org/resource/葛飾北斎>  }
# UNION { ?CreativeWork ?has_author <http://dbpedia.org/resource/Hokusai>  }
# UNION { ?CreativeWork ?has_author <http://www.wikidata.org/entity/Q5586>  }
# UNION { ?CreativeWork ?has_author <http://rdf.freebase.com/ns/m.0bwf4>  } .
#} LIMIT 1500

#PREFIX wd: <http://www.wikidata.org/entity/>
#PREFIX schema: <http://schema.org/>
#PREFIX dbo: <http://dbpedia.org/ontology/>
#SELECT DISTINCT ?CreativeWork ?pred ?obj WHERE {
#  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ja". }
#  ?CreativeWork ?has_title "凱風快晴"@ja .
#  ?CreativeWork ?pred ?obj .
#  { ?CreativeWork a schema:CreativeWork  } UNION
#  { ?CreativeWork wdt:P31 wd:Q17537576  } UNION
#  { ?CreativeWork a dbo:Creative_work  } .
#  { ?CreativeWork ?has_author <http://dbpedia.org/resource/Hokusai>  } UNION
#  { ?CreativeWork ?has_author <http://www.wikidata.org/entity/Q5586>  } UNION
#  { ?CreativeWork ?has_author <http://ja.dbpedia.org/resource/葛飾北斎>  } UNION
#  { ?CreativeWork ?has_author <http://rdf.freebase.com/ns/m.0bwf4>  } .
#} LIMIT 1500


exit(0)
ipdb.set_trace()

lemmas = ["chair", "law", "right", "beaver"]
things = []
for lemma in lemmas:
    thing = Thing(
        label=lemma,
        limit=100,
        endpoints=[Endpoint.wikidata, Endpoint.dbpedia, Endpoint.dbpedia_fr],
        query_language=Lang.English
    )

    thing.query(check_type=False, strict_mode=False)
    thing.find_more_about()
    things.append(thing)

book = Book(
    author='Virginia Woolf',
    title="A Room of One's Own",
    endpoints=[e for e in Endpoint])
book.query()

#for e in Endpoint:
#    assert fuzz.token_sort_ratio(expected_queries[e], thing.query_builder.queries[e]) == 100

ipdb.set_trace()






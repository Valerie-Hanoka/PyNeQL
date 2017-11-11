#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
core.py is part of the project PyNeQL
Author: Valérie Hanoka

"""
import logging
from querybuilder import RDFTripletBuilder

rdf2 = RDFTripletBuilder(
    prefixes=[
        " t3st_1234  : <http://foo.org/bar/1.1/buz.owl#>  .",
        "xsd: <http://www.w3.org/2001/XMLSchema#>"])

import ipdb; ipdb.set_trace()


# query = pyneql.Query()
# query.query(name, language)
# query.set_endpoints( endpoints_list )
# query.add_filters( filters_list )
# query.limit( limit_int )
# query.result_language( lang_list)
# query.result_types( type_list )


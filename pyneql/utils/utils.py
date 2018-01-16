#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
utils.py is part of the project PyNeQL
Author: Valérie Hanoka

"""
from copy import deepcopy
from unicodedata import normalize

import re

# ----  Exceptions ---- #
class QueryException(Exception):
    pass


class NameSpaceException(QueryException):
    pass

# ---- Data structures ---- #

def merge_two_dicts_in_lists(x, y):
    """Given two dicts (with string keys),
    merge them into a new dict as a deep copy.
    In cases of duplicate keys, values are appended in lists.
    Ex.:
    >>> dic_y = {'both': {'both_y_diff' : 'bar', 'both_same': 'same_y'}, 'only_y': 'only_y'}
    >>> dic_x = {'both': {'both_x_diff' : 'foo', 'both_same': 'same_x'}, 'only_x': {'only_x' : 'baz'}}
    >>> merge_two_dicts(dic_x, dic_y)
    >>> {'both': {
    >>>      'both_same': ['same_x', 'same_y'],
    >>>      'both_x_diff': 'foo',
    >>>      'both_y_diff': 'bar'},
    >>>  'only_x': {'only_x': 'baz'},
    >>>  'only_y': 'only_y'}
    :param x: First dictionary
    :param y: Second dictionary
    :return: The recursive merge of x and y, appending values in list in case of duplicate keys."""
    if not isinstance(y, dict):
        return y
    result = deepcopy(x)
    for k, v in y.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = merge_two_dicts_in_lists(result[k], v)
        else:
            if isinstance(v, dict):
                result[k] = deepcopy(v)
            else:
                v = deepcopy(v)
                existing_v = deepcopy(result.get(k, []))
                if existing_v:
                    v = v if isinstance(v, list) else [v]
                    existing_v = existing_v if isinstance(existing_v, list) else [existing_v]
                    result[k] = existing_v+v
                else:
                    result[k] = v
    return result


def merge_two_dicts_in_sets(x, y):
    """Given two dicts (with string keys),
    merge them into a new dict as a deep copy.
    In cases of duplicate keys, values are added into a set.
    Ex.:
    >>> dic_y = {'both': {'both_y_diff' : 'bar', 'both_same': 'same_y'}, 'only_y': 'only_y'}
    >>> dic_x = {'both': {'both_x_diff' : 'foo', 'both_same': 'same_x'}, 'only_x': {'only_x' : 'baz'}}
    >>> merge_two_dicts(dic_x, dic_y)
    >>> {'both': {
    >>>      'both_same': set(['same_x', 'same_y']),
    >>>      'both_x_diff': 'foo',
    >>>      'both_y_diff': 'bar'},
    >>>  'only_x': {'only_x': 'baz'},
    >>>  'only_y': 'only_y'}
    :param x: First dictionary
    :param y: Second dictionary
    :return: The recursive merge of x and y, appending values in list in case of duplicate keys."""
    if not isinstance(y, dict):
        return y
    result = deepcopy(x)
    for k, v in y.items():
        if k in result and isinstance(result[k], dict):
                result[k] = merge_two_dicts_in_sets(result[k], v)
        else:
            if isinstance(v, dict):
                result[k] = deepcopy(v)
            else:
                v = deepcopy(v)
                existing_v = deepcopy(result.get(k, set([])))
                if existing_v:
                    v = v if isinstance(v, set) else set([v])
                    existing_v = existing_v if isinstance(existing_v, set) else set([existing_v])
                    result[k] = existing_v | v
                else:
                    result[k] = v
    return result


# ---- Stringology ---- #
def normalize_str(s):
    """ Remove leading and trailing and multiple whitspaces from a string s.
    :param s: a string or unicode
    :return: the unicode normalised version of s
    """
    if isinstance(s, str):
        s = unicode(s.strip(), 'utf-8')
    else:
        s = s.strip()
    s = normalize('NFC', s)
    return u' '.join(s.split())


RE_CONTAINS_A_DATE = re.compile('^[0-9\-]+[0-9TZ:\-]*$')
def contains_a_date(s):
    """ Detects if a string contains a date.
    :param s: a string
    :return: True if s contains a date, False otherwise.
    """
    return RE_CONTAINS_A_DATE.search(s)

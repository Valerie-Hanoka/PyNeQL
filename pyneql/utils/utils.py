#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
utils.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

import six
from copy import deepcopy
from unicodedata import normalize
import re

try:
    basestring
except NameError:
    basestring = str


# ----  Exceptions ---- #
class QueryException(Exception):
    pass


class NameSpaceException(QueryException):
    pass

# ---- Data structure identification --- #

def is_listlike(element):
    """Identify objects that acts like lists (list, tuple, set, ...)
    but are *not* strings.
    """

    if isinstance(element, basestring):
        return False
    else:
        try:
            element.__iter__()
            return True
        except AttributeError:
            return False

# ---- Data structures ---- #

def merge_two_dicts_in_lists(x, y):
    """Given two dicts (with string keys),
    merge them into a new dict as a deep copy.
    In cases of duplicate keys, values are appended in lists.

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
    for k, v in six.iteritems(y):
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
    s = u'%s' % s.strip()
    s = normalize('NFC', s)
    return u' '.join(s.split())


RE_CONTAINS_A_DATE = re.compile('^[0-9\-]+[0-9TZ:\-]*$')
def contains_a_date(s):
    """ Detects if a string contains a date.

    :param s: a string
    :return: True if s contains a date, False otherwise.
    """
    return RE_CONTAINS_A_DATE.search(s)


RE_LITERAL_LANGUAGE = re.compile('(?P<lit>.*?) _\(@(?P<lang>.*)\)')
def parse_literal_with_language(literal_with_language_str):
    """
    At some point, literals in the result set are formated as follow:
    "literal _(@lang)". This function parses this string if possible,
    and returns a couple (litteral, language).
    :param literal_with_language_str: The string of the form "literal _(@lang)"
    :return: a couple (literal, lang) if the language is detected,
    (literal, None) otherwise.
    """
    match = re.match(RE_LITERAL_LANGUAGE, literal_with_language_str)
    if match:
        return match.groupdict().get('lit'), match.groupdict().get('lang')
    else:
        return literal_with_language_str, None

# ----- Eye sugar ----- #
def pretty_print_utf8(result_dataset):
    """For debug & documentation purpose"""
    for key in sorted(result_dataset.keys()):
        utf8_values = recursive_pretty_print(result_dataset[key])
        print("%s: ([ %s ])," % (key.encode('utf8'), utf8_values))

def recursive_pretty_print(element):

    utf_8 = ""
    if isinstance(element, set) or isinstance(element, list):
        for e in element:
            if utf_8:
                utf_8 = ','.join([recursive_pretty_print(e), utf_8])
            else:
                utf_8 = recursive_pretty_print(e)
    else:
        try:
            int(element)
        except:
            utf_8 = '"%s"' % str(element).encode('utf8')
        else:
            utf_8 = '%s' % element.encode('utf8')
    return utf_8
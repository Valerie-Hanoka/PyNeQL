#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_utils.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from pyneql.utils.utils import (
    merge_two_dicts_in_lists,
    merge_two_dicts_in_sets,
    normalize_str
)


def test_utils_merge_two_dicts_in_list1():
    """Recursive merge & append dict values: Should pass"""

    dic_y = {'both': {'both_y_diff': 'bar', 'both_same': 'same_y'}, 'only_y': 'only_y'}
    dic_x = {'both': {'both_x_diff': 'foo', 'both_same': 'same_x'}, 'only_x': {'only_x': 'baz'}}
    merged = merge_two_dicts_in_lists(dic_x, dic_y)

    truth = {
        'both': {'both_same': ['same_x', 'same_y'],
                 'both_x_diff': 'foo',
                 'both_y_diff': 'bar'},
        'only_x': {'only_x': 'baz'},
        'only_y': 'only_y'
    }
    assert merged == truth


def test_utils_merge_two_dicts_in_list2():
    """Recursive merge & append dict values: Should pass"""

    x = {'both1': 'botha1x', 'both2': 'botha2x', 'only_x': 'only_x'}
    y = {'both1': 'botha1y', 'both2': 'botha2y', 'only_y': 'only_y'}
    merged = merge_two_dicts_in_lists(x, y)
    truth = {
        'both1': ['botha1x', 'botha1y'],
        'both2': ['botha2x', 'botha2y'],
        'only_x': 'only_x',
        'only_y': 'only_y'
    }
    assert merged == truth



def test_utils_merge_two_dicts_in_sets1():
    """Recursive merge & append dict values: Should pass"""

    dic_y = {'both': {'both_y_diff': 'bar', 'both_same': 'same_y'}, 'only_y': 'only_y'}
    dic_x = {'both': {'both_x_diff': 'foo', 'both_same': 'same_x'}, 'only_x': {'only_x': 'baz'}}
    merged = merge_two_dicts_in_sets(dic_x, dic_y)

    truth = {
        'both': {'both_same': set(['same_x', 'same_y']),
                 'both_x_diff': 'foo',
                 'both_y_diff': 'bar'},
        'only_x': {'only_x': 'baz'},
        'only_y': 'only_y'
    }
    assert merged == truth


def test_utils_merge_two_dicts_in_sets2():
    """Recursive merge & append dict values: Should pass"""

    x = {'both1': 'botha1x', 'both2': 'botha2', 'only_x': 'only_x'}
    y = {'both1': 'botha1y', 'both2': 'botha2', 'only_y': 'only_y'}
    merged = merge_two_dicts_in_sets(x, y)
    truth = {
        'both1': set(['botha1x', 'botha1y']),
        'both2': set(['botha2']),
        'only_x': 'only_x',
        'only_y': 'only_y'
    }

    import pprint
    pprint.pprint(merged)

    assert merged == truth



def test_utils_normalize_str():
    """Utils - Naïve string normalisation: Should pass """

    no_norm ="   A form of logical, intuitive reasoning   to deduce the nature of an uncertain thing or" \
      " situation, usually in the absence or in     spite of concrete evidence. Adapted from the saying, " \
      "If it looks like     a duck, swims like a duck, and   quacks like a duck, then it's probably a " \
      "                                      duck.                                                       " \
      "" \
      "" \
      "                                                                                                  "
    normalised = normalize_str(no_norm)
    well_normalised = u"A form of logical, intuitive reasoning to deduce the nature of an uncertain" \
                      u" thing or situation, usually in the absence or in spite of concrete evidence." \
                      u" Adapted from the saying, If it looks like a duck, swims like a duck, " \
                      u"and quacks like a duck, then it's probably a duck."

    assert isinstance(normalised, unicode)
    assert well_normalised == normalised
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_utils.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

from pyneql.utils.utils import (
    merge_two_dicts_in_lists,
    merge_two_dicts_in_sets,
    normalize_str,
    is_listlike,
    parse_literal_with_language
)

def test_utils_is_listlike():
    """Is a python object iterable but not a string ?: should pass"""
    ok = [(1, 2, 3), [1, 2, 3], {1, 3, 2}, iter([1, 2, 3])]
    ok_size = len(ok)
    not_ok = [123, "123", u'123']

    assert len([is_listlike(e) for e in ok]) == ok_size
    assert not any([is_listlike(e) for e in not_ok])

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

    assert well_normalised == normalised


def test_utils_parse_literal_with_language():
    """Utils - parse a literal with language: Should pass """

    literal_list = [
        'Аддис-Абеба _(@tg)', 'Addis Ababa _(@tr)', 'Ադիս Աբեբա _(@hy)',
        'Аддис-Абеба _(@uk)', 'Addis Abeba _(@it)', 'Аддис-Абеба _(@udm)',
        'Addis Abeba _(@dsb)', 'Адыс-Абэба _(@be-tarask)', 'Adis Abeba _(@kg)',
        'ཨ་ཌི་སི་ཨ་བ་བ། _(@bo)', 'Аддис-Абеба _(@ru)', 'اديس ابابا _(@arz)', 'Addis Abeba _(@eu)',
        'Addis Abeba _(@srn)', 'Addis Abeba _(@kab)', 'Аддис-Абеба _(@mn)',
        'אדיס אבאבא _(@yi)', 'अदिस अबाबा _(@mr)', 'Addis Abeba _(@cs)',
        'Addis Abeba _(@nn)', 'Addis Abeba _(@pms)', 'Adis Abeba _(@hr)',
        'ادیس ابابا _(@ur)', 'Адис Абеба _(@bg)', 'Addis Abeba _(@vro)',
        'അഡിസ് അബെബ _(@ml)', 'Adis Abeba _(@diq)', 'Addis Ababa _(@is)',
        'Addis Ababa _(@da)', 'آدیس آبابا _(@fa)', 'ადის-აბება _(@ka)',
        '亚的斯亚贝巴 _(@zh-hans)', 'အာဒစ် အာဘာဘာမြို့ _(@my)', 'అద్దిస్ అబాబా _(@te)',
        'Addis-Abeba _(@fr)', 'Addis Abeba _(@et)', 'Addis-Abeba _(@wo)',
        'Addisz-Abeba _(@hu)', 'Addis Abeba _(@oc)', '亚的斯亚贝巴 _(@zh)', 'Addis Ababa _(@cy)',
        'Addis Abeba _(@ca)', 'Адис _(@sr)', 'Addis-Abeba _(@uz)', 'אדיס אבבה _(@he)',
        '亚的斯亚贝巴 _(@wuu)', 'Addis Ababa _(@ig)', 'Addis Ababa _(@yo)',
        'Addis Abeba _(@nb)', 'Addis Abeba _(@rm)', 'Adis-Abebo _(@eo)',
        'Addis Ab@fi)', 'ಅಡಿಸ್ ಅಬಾಬ _(@kn)', 'アディスアベバ _(@ja)',
        'Аддис-Абеба _(@kk)', 'Addis Ababa _(@id)', 'Addis Ababa _(@hif)',
        'ਆਦਿਸ ਆਬਬਾ _(@pa)', 'Adis Abeba _(@pt-br)', 'Addis Abeba _(@sc)', 'Addis (@mg)',
        'Addis Abeba _(@lmo)', 'Adís Abeba _(@gl)', 'Addis Abeba _(@lb)', 'Addis Abeba _(@nl)',
        'ادیس ابابا _(@pnb)', 'Аддис-Абеба _(@ky)', 'Adis Abeba _(@bs)', 'Адис Абеба _(@mk)',
        '阿迪斯阿貝yue)', 'Addis Ababa _(@en)', 'แอดดิสอาบาบา _(@th)', 'Addis Ababa _(@ms)',
        'Addis Ababa _(@pap)', 'Addis Ababa _(@sn)', 'আদ্দিস আবাবা _(@bn)', 'Adís Abeba _(@es)',
        'Addis Abeba _(@ro)', 'அடிஸ் அபாபா _(@ta)', 'Adis-Abeba _(@ht)', 'Addis Ababa _(@fo)',
        'Аддис-Абеба _(@ce)', 'ადის-აბება _(@xmf)', 'Addis Abeba _(@br)', 'Neanthopolis _(@la)',
        'Addis Abeba _(@om)', 'Addis Abeba _(@af)', 'Addis Abeba _(@hsb)', 'Addis Ababa _(@ha)']

    for literal in literal_list:
        assert len(parse_literal_with_language(literal)) > 0

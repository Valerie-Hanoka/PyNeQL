#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
utils.py is part of the project PyNeQL
Author: Valérie Hanoka

"""


class QueryException(Exception):
    pass


class NameSpaceException(QueryException):
    pass


def normalize_str(s):
    """ Remove leading and trailing and multiple whitspaces from a string s.
    Return the unicode equivalent of s."""
    s = s.strip()
    return u' '.join(s.split())

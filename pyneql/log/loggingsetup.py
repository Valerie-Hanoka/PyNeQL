#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
loggingsetup.py is part of the project PyNeQL
Author: Valérie Hanoka

"""

import logging
import os
import json
import logging.config


def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Setup logging configuration

    :param default_path: Default path of the json logging configuration file
    :param default_level:
    :param env_key:
    """
    path = default_path
    value = os.getenv(env_key)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def highlight_str(s, highlight_type=None):
    """
    Highlighter for logging using ANSI escape code.

    :param s: the element to highlight in the logs
    :param highlight_type: types of highlight
    :return: an highlighted string
    """
    if highlight_type == 'query':
        return "\x1b[31;1m %s \x1b[0m" % s
    elif highlight_type == 'triple':
        return "\x1b[32;1m %s \x1b[0m" % s
    else:
        return "\x1b[34;1m %s \x1b[0m" % s

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tags.py
# Udacity.com -- "Data Wrangling with MongoDB"
# OpenStreetMap Data Case Study
#
# Matthew T. Banbury
# matthewbanbury@gmail.com

"""
Checks the "k" value for each "<tag>" for validity or potential problems in
MongoDB. See the 3 regular expressions that check for certain patterns in the tags.

The data model changes to expand the "addr:street" type of keys to a dictionary
like this:

{"address": {"street": "Some value"}}
"""
import xml.etree.cElementTree as ET
import pprint
import re


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        if re.search(problemchars, element.attrib['k']):
            keys['problemchars'] += 1
        elif re.search(lower_colon, element.attrib['k']):
            keys['lower_colon'] += 1
        elif re.search(lower, element.attrib['k']):
            keys['lower'] += 1
        else:
            keys['other'] += 1
    return keys

# Used to pass autograder on Udacity.com
def old_process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for __, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    parser = ET.iterparse(filename)
    for __, elem in parser:
        keys = key_type(elem, keys)
        # It's safe to call clear() here because no
        # descendants will be accessed
        elem.clear()
    del parser
    return keys


def main_test():
    keys = process_map('charlotte.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 227362,
                    'lower_colon': 290941,
                    'other': 148852,
                    'problemchars': 0}


def example_test():
    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 11692,
                    'lower_colon': 14261,
                    'other': 1059,
                    'problemchars': 0}


if __name__ == "__main__":
    example_test()

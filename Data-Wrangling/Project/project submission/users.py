#!/usr/bin/env python
# -*- coding: utf-8 -*-

# users.py
# Udacity.com -- "Data Wrangling with MongoDB"
# OpenStreetMap Data Case Study
#
# Matthew T. Banbury
# matthewbanbury@gmail.com

"""
Finds out how many unique users have contributed to the map in this
particular area.

Returns a set of unique user IDs ("uid").
"""
import xml.etree.cElementTree as ET
import pprint
import re


def get_user(element):
    if 'uid' in element.attrib:
        return element.attrib['uid']

# Used to pass autograder on Udacity.com
def old_process_map(filename):
    users = set()
    for __, element in ET.iterparse(filename):
        uid = get_user(element)
        if uid != None:
            users.add(uid)
    return users


def process_map(filename):
    users = set()
    parser = ET.iterparse(filename)
    for __, elem in parser:
        uid = get_user(elem)
        if uid != None:
            users.add(uid)
        # It's safe to call clear() here because no
        # descendants will be accessed
        elem.clear()
    del parser
    return users


def main_test():
    users = process_map('charlotte.osm')
    pprint.pprint(users)
    assert len(users) == 351


def example_test():
    users = process_map('example.osm')
    pprint.pprint(users)
    assert len(users) == 115


if __name__ == "__main__":
    example_test()

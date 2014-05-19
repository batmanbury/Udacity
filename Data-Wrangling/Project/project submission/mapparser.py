#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mapparser.py
# Udacity.com -- "Data Wrangling with MongoDB"
# OpenStreetMap Data Case Study
#
# Matthew T. Banbury
# matthewbanbury@gmail.com

"""
Uses iterative parsing to process the map file and find out how many of each tag
there are. The output is a dictionary with tag names as keys and the number of
times they can be encountered in the map values.
"""
import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):
    tags = {}
    parser = ET.iterparse(filename)
    for __, elem in parser:
        if elem.tag in tags:
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
        # It's safe to call clear() here because no
        # descendants will be accessed
        elem.clear()
    del parser
    return tags


def main_test():
    tags = count_tags('charlotte.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                    'member': 12112,
                    'nd': 1623443,
                    'node': 1471350,
                    'osm': 1,
                    'relation': 321,
                    'tag': 667155,
                    'way': 84502}
                    # 3858885 total


def example_test():
    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'member': 7125,
                    'meta': 1,
                    'nd': 52969,
                    'node': 46721,
                    'note': 1,
                    'osm': 1,
                    'relation': 44,
                    'tag': 27012,
                    'way': 3781}
                    # 137655 total

if __name__ == "__main__":
    main_test()

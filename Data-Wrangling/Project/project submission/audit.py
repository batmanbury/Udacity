#!/usr/bin/env python
# -*- coding: utf-8 -*-

# audit.py
# Udacity.com -- "Data Wrangling with MongoDB"
# OpenStreetMap Data Case Study
#
# Matthew T. Banbury
# matthewbanbury@gmail.com

"""
- Audits the OSMFILE and changes the variable 'mapping' to reflect the changes
    needed to fix the unexpected street types to the appropriate ones in the
    expected list. Mappings have been added only for the actual problems found
    in this OSMFILE, not for a generalized solution, since that may and will
    depend on the particular area being audited.
- The update function fixes the street name. It takes a string with a street
    name as an argument and returns the fixed name.
"""
from collections import defaultdict
import xml.etree.cElementTree as ET
import pprint
import re


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
expected = ["Street", "Avenue", "Boulevard", "Drive",
            "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Cirle",
            "Cove", "Highway", "Park", "Way", "South"]

# Updated mapping reflects changes needed in charlotte.osm file
mapping = { "E": "East",
            "W": "West",
            "N": "North",
            "S": "South",
            "Rd": "Road",
            "Rd.": "Road",
            "ln": "Lane",
            "ln.": "Lane",
            "Ln": "Lane",
            "Ln.": "Lane",
            "Dr": "Drive",
            "Dr.": "Drive",
            "St": "Street",
            "St.": "Street",
            "Ste": "Suite",
            "Ste.": "Suite",
            "Cir": "Circle",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Hwy": "Highway",
            "Hwy.": "Highway",
            "Pky": "Parkway",
            "Pky.": "Parkway",
            "Fwy": "Freeway",
            "Fwy.": "Freeway",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard"
            }


def audit_street_type(street_types, street_name):
    """
    Adds potentially problematic street names to
    list 'street_types'
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """
    Returns a list of problematic street type values
    for use with the update() name mapping.
    """
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    parser = ET.iterparse(osm_file, events=("start",))
    for event, elem in parser:
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
        # Safe to clear() now that descendants have been accessed
        elem.clear()
    del parser
    return street_types


def update(name, mapping):
    """
    Implemented in data.py
    Updates ALL substrings in string 'name' to
    their values in dictionary 'mapping'
    """
    words = name.split()
    for w in range(len(words)):
        if words[w] in mapping:
            if words[w-1].lower() not in ['suite', 'ste.', 'ste']: # For example, don't update 'Suite E' to 'Suite East'
                words[w] = mapping[words[w]]
    name = " ".join(words)
    return name

# EXPERIMENTAL UNUSED METHOD
# Opted not to use in data.py over the more generalized
# and more optimal 'update()' method above
def update_name(name, mapping):
    """
    If the last substring of string 'name' is an int,
    updates all substrings in 'name', else updates
    only the last substring.
    """
    m = street_type_re.search(name)
    m = m.group()
    # Fix all substrings in an address ending with a number.
    # Example: 'S Tryon St Ste 105' to 'South Tryon Street Suite 105'
    try:
        __ = int(m)
        words = name.split()[:-1]
        for w in range(len(words)):
            if words[w] in mapping:
                words[w] = mapping[words[w]]
        words.append(m)
        address = " ".join(words)
        return address
    # Otherwise, fix only the last substring in the address
    # Example: 'This St.' to 'This Street'
    except ValueError:        
        i = name.index(m)
        if m in mapping:
            name = name[:i] + mapping[m]
    return name


def main_test():
    st_types = audit("charlotte.osm")
    assert len(st_types) == 19
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update(name, mapping)
            print name, "=>", better_name
            if name == "West Stanly St.":
                assert better_name == "West Stanly Street"
            if name == "S Tryon St Ste 105":
                assert better_name == "South Tryon Street Suite 105"


def example_test():
    st_types = audit("example.osm")
    assert len(st_types) == 6
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update(name, mapping)
            print name, "=>", better_name
            if name == "Winthrop Ave":
                assert better_name == "Winthrop Avenue"
            if name == "W 9th St":
                assert better_name == "West 9th Street"


if __name__ == '__main__':
    example_test()

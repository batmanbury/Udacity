#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit the
datatypes that can be found in some particular fields in the dataset.

The possible types of values can be:
- 'NoneType' if the value is a string "NULL" or an empty string ""
- 'list', if the value starts with "{"
- 'int', if the value can be cast to int
- 'float', if the value can be cast to float, but is not an int
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and the
datatypes that can be found in the field. All the data initially is a string, so
you have to do some checks on the values first.

"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label",
          "isPartOf_label", "areaCode", "populationTotal", "elevation",
          "maximumElevation", "minimumElevation", "populationDensity",
          "wgs84_pos#lat", "wgs84_pos#long", "areaLand", "areaMetro", "areaUrban"]

def audit_file(filename, fields):
    fieldtypes = {}
    for field in fields:
        fieldtypes[field] = set([])

    # YOUR CODE HERE
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        
        #skipping the extra metadata
        for i in range(3):
            reader.next()

        # processing file
        for row in reader:
            for field in fields:
                value = row[field]
                if value == 'NULL' or value == '':
                    fieldtypes[field].add(type(None))
                elif value.startswith('{'):
                    fieldtypes[field].add(list)
                else:
                    try:
                        value = int(value)
                        fieldtypes[field].add(int)
                    except ValueError:
                        try:
                            value = float(value)
                            fieldtypes[field].add(float)
                        except ValueError:
                            fieldtypes[field].add(str)

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()

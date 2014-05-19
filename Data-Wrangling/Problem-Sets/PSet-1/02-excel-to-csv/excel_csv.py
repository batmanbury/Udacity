# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

'''
Station|Year|Month|Day|Hour|Max Load
COAST|2013|01|01|10|12345.6
EAST|2013|01|01|10|12345.6
FAR_WEST|2013|01|01|10|12345.6
NORTH|2013|01|01|10|12345.6
NORTH_C|2013|01|01|10|12345.6
SOUTHERN|2013|01|01|10|12345.6
SOUTH_C|2013|01|01|10|12345.6
WEST|2013|01|01|10|12345.6
'''

import xlrd
import os
import csv
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    
    maxvalues = {} # structure: {label: [maxload(0), time(1)]}
    for col in range(1, sheet.ncols - 1):
        label = sheet.cell_value(0, col)
        column = sheet.col_values(col, start_rowx=1, end_rowx=sheet.nrows)
        maxvalues[label] = [max(column)]
        maxrownum = column.index(max(column)) + 1
        maxvalues[label].append(sheet.cell_value(maxrownum, 0))
    
    stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH', 'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    for station in stations:
        row = [station]
        time = xlrd.xldate_as_tuple(maxvalues[station][1], 0)
        for index in range(len(time[:4])):
            row.append(time[index])
        row.append(maxvalues[station][0])
        data.append(row)

    print data
    return data


def save_file(data, filename):
    with open(filename, 'w') as csvfile:
        datawriter = csv.writer(csvfile, delimiter = '|')
        datawriter.writerow(['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load'])
        datawriter.writerows(data)


def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    ans = {'FAR_WEST': {'Max Load': "2281.2722140000024", 'Year': "2013", "Month": "6", "Day": "26", "Hour": "17"}}
    
    fields = ["Year", "Month", "Day", "Hour", "Max Load"]
    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            s = line["Station"]
            if s == 'FAR_WEST':
                for field in fields:
                    assert ans[s][field] == line[field]

        
test()

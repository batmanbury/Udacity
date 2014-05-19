#!/usr/bin/env python
# -*- coding: utf-8 -*-
# All your changes should be in the 'extract_airports' function
# It should return a list of airport codes, excluding any combinations like "All"

from bs4 import BeautifulSoup
html_page = "options.html"


def extract_airports(page):
    data = []
    
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html)
        option_tags = soup.find_all('option')
        for tag in option_tags:
            if len(tag['value']) == 3 and tag['value'] != 'All':
                data.append(tag['value'])

    return data


def test():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

test()

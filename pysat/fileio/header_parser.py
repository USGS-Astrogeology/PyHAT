# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 13:35:56 2015

@author: rbanderson
"""


def header_parser(row, delim):
    # get rid of various unwanted characters
    badlist = ['#', '^', "'", '*']
    for i in badlist:
        row = row.replace(i, '')
    row.strip()

    if delim in row:
        tmp = row.split(delim)
        label = tmp[0].strip().lower().replace('  ', '_').replace(' ', '_')
        data = row.split(tmp[0] + delim)[1].strip()
        headinfo = {label: data}
    else:
        headinfo = {}
    return headinfo

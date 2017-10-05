# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 09:51:51 2015

@author: rbanderson

This function uses the pandas merge ability to look up metadata for an existing dataframe in a csv file
If lookupfile is a list, then each file will be read and concatenated together. Alternatively, a dataframe can be provided directly.
The default settings are for looking up ChemCam CCS csv data in the ChemCam master list files, matching on sclock value
"""
import pandas as pd
def lookup(df,lookupfile=None,lookupdf=None,sep=',',skiprows=1,left_on='sclock',right_on='Spacecraft Clock'):
#TODO: automatically determine the number of rows to skip to handle ccam internal master list and PDS "official" master list formats
    if lookupfile is not None:
        # this loop concatenates together multiple lookup files if provided
        # (mostly to handle the three different master lists for chemcam)
        for x in lookupfile:
            try:
                tmp = pd.read_csv(x, sep=sep, skiprows=skiprows, error_bad_lines=False)
                lookupdf = pd.concat([lookupdf, tmp])
            except:
                lookupdf = pd.read_csv(x, sep=sep, skiprows=skiprows, error_bad_lines=False)
    metadata = df['meta']

    metadata = metadata.merge(lookupdf, left_on=left_on, right_on=right_on, how='left')

    # remove metadata columns that already exist in the data frame to avoid non-unique columns
    meta_cols = set(metadata.columns.values)
    meta_cols_keep = list(meta_cols - set(df['meta'].columns.values))
    metadata = metadata[meta_cols_keep]

    # make metadata into a multiindex
    metadata.columns = [['meta'] * len(metadata.columns), metadata.columns.values]
    # give it the same indices as the df
    metadata.index = df.index
    # combine the df and the new metadata
    df = pd.concat([metadata, df], axis=1)
    return df

# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 12:51:34 2015

@author: rbanderson
"""
import numpy as np
from sklearn import cross_validation


def random(df, nfolds=5, seed=10, groupby=None):
    df['Folds'] = 'None'  # Create an entry in the data frame that holds the folds
    foldslist = np.array(df['Folds'])
    if groupby == None:  # if no column name is listed to group on, just create random folds
        n = len(df.index)
        folds = cross_validation.KFold(n, nfolds, shuffle=True, random_state=seed)
        i = 1
        for train, test in folds:
            foldslist[test] = 'Fold' + str(i)
            i = i + 1

    else:
        # if a column name is provided, get all the unique values and define folds
        # so that all rows of a given value fall in the same fold
        # (this is useful to ensure that training and test data are truly independent)
        unique_inds = np.unique(df[groupby])
        folds = cross_validation.KFold(len(unique_inds), nfolds, shuffle=True, random_state=seed)
        foldslist = np.array(df['Folds'])
        i = 1
        for train, test in folds:
            tmp = unique_inds[test]
            tmp_full_list = np.array(df[groupby])
            tmp_ind = np.in1d(tmp_full_list, tmp)
            foldslist[tmp_ind] = 'Fold' + str(i)
            i = i + 1

    df['Folds'] = foldslist
    return df

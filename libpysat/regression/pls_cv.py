# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:16:11 2016
This function is used to run cross validation using PLS 
to help choose the optimal number of components. Folds are stratified 
according to a user-specified column

@author: rbanderson
"""
import matplotlib.pyplot as plot
import numpy as np
from libpysat.spectral.meancenter import meancenter
from sklearn.cross_decomposition.pls_ import PLSRegression
from sklearn.cross_validation import LeaveOneLabelOut


def pls_cv(Train, Test=None, nc=20, nfolds=5, ycol='SiO2', doplot=True, outpath='.', plotfile='pls_cv.png'):
    # create empty arrays for the RMSE values
    pls_rmsecv = np.empty(nc)
    pls_rmsec = np.empty(nc)
    # If there is a test set provided, create the RMSEP array to hold test set errors
    if Test is not None:
        pls_rmsep = np.empty(nc)

    # loop through each number of components
    for i in range(1, nc + 1):
        print('nc=' + str(i))
        Train[('meta', ycol + '_cv_PLS_nc' + str(
            i))] = 0  # create a column to hold the PLS cross validation results for this nc
        Train[
            ('meta', ycol + '_PLS_nc' + str(i))] = 0  # create a column to hold the PLS training set results for this nc
        if Test is not None:
            Test[
                ('meta', ycol + '_PLS_nc' + str(i))] = 0  # create a column to hold the PLS test set results for this nc

        # Do the cross validation
        cv_iterator = LeaveOneLabelOut(
            Train[('meta', 'Folds')])  # create the iterator for cross validation within the training data

        for train, holdout in cv_iterator:  # Iterate through each of the folds in the training set
            cv_train = Train.iloc[train]
            cv_holdout = Train.iloc[holdout]

            # Do PLS for this number of components
            cv_train_centered, cv_train_mean_vect = meancenter(cv_train)  # mean center training data
            cv_holdout_centered, cv_holdout_mean_vect = meancenter(cv_holdout,
                                                                   previous_mean=cv_train_mean_vect)  # apply same mean centering to holdout data
            pls = PLSRegression(n_components=i, scale=False)
            pls.fit(cv_train_centered['wvl'], cv_train_centered['meta'][ycol])
            y_pred_holdout = pls.predict(cv_holdout_centered['wvl'])
            Train.set_value(Train.index[holdout], ('meta', ycol + '_cv_PLS_nc' + str(i)), y_pred_holdout)

        pls_rmsecv[i - 1] = np.sqrt(
            np.mean(np.subtract(Train[('meta', ycol)], Train[('meta', ycol + '_cv_PLS_nc' + str(i))]) ** 2, axis=0))

        # Do train and test set PLS predictions for this number of components
        Train_centered, Train_mean_vect = meancenter(Train)
        pls = PLSRegression(n_components=i, scale=False)
        pls.fit(Train_centered['wvl'], Train_centered['meta'][ycol])

        y_pred = pls.predict(Train_centered['wvl'])
        Train.set_value(Train.index, ('meta', ycol + '_PLS_nc' + str(i)), y_pred)
        pls_rmsec[i - 1] = np.sqrt(
            np.mean(np.subtract(Train[('meta', ycol)], Train[('meta', ycol + '_PLS_nc' + str(i))]) ** 2, axis=0))

        if Test is not None:
            Test_centered, Train_mean_vect = meancenter(Test, previous_mean=Train_mean_vect)
            y_pred = pls.predict(Test_centered['wvl'])
            Test.set_value(Test.index, ('meta', ycol + '_PLS_nc' + str(i)), y_pred)
            pls_rmsep[i - 1] = np.sqrt(
                np.mean(np.subtract(Test[('meta', ycol)], Test[('meta', ycol + '_PLS_nc' + str(i))]) ** 2, axis=0))

    if doplot == True:
        plot.figure()
        plot.title(ycol)
        plot.xlabel('# of components')
        plot.ylabel(ycol + ' RMSE (wt.%)')
        plot.plot(range(1, nc + 1), pls_rmsecv, label='RMSECV', color='r')
        plot.plot(range(1, nc + 1), pls_rmsec, label='RMSEC', color='b')
        if Test is not None:
            plot.plot(range(1, nc + 1), pls_rmsep, label='RMSEP', color='g')
        plot.legend(loc=0, fontsize=6)
        plot.savefig(outpath + '/' + plotfile, dpi=600)

    rmses = {'RMSEC': pls_rmsec, 'RMSECV': pls_rmsecv}
    if Test is not None:
        rmses['RMSEP'] = pls_rmsep
    return rmses

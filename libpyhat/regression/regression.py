# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 11:31:46 2016

@author: rbanderson
"""
import copy
import traceback
import numpy as np
import sklearn.kernel_ridge as kernel_ridge
import sklearn.linear_model as linear
import sklearn.svm as svm
import sklearn.gaussian_process as gp
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import GradientBoostingRegressor

class regression:
    def __init__(self, method, params, i=0):
        self.algorithm_list = ['PLS',
                               'GP',
                               'OLS',
                               'OMP',
                               'Lasso',
                               'Elastic Net',
                               'Ridge',
                               'Bayesian Ridge',
                               'ARD',
                               'LARS',
                               'LASSO LARS',
                               'SVR',
                               'KRR',
                               'GBR'
                               ]
        self.method = method
        self.outliers = None
        self.ransac = False

        #print(params)
        if self.method[i] == 'PLS':
            self.model = PLSRegression(**params[i])

        if self.method[i] == 'OLS':
            self.model = linear.LinearRegression(**params[i])

        if self.method[i] == 'OMP':
          # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            self.model = linear.OrthogonalMatchingPursuit(**params_temp)

        if self.method[i] == 'LASSO':
            # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            self.model = linear.Lasso(**params_temp)

        if self.method[i] == 'Elastic Net':
            params_temp = copy.copy(params[i])
            self.model = linear.ElasticNet(**params_temp)

        if self.method[i] == 'Ridge':
            # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            self.model = linear.Ridge(**params_temp)

        if self.method[i] == 'BRR':
            self.model = linear.BayesianRidge(**params[i])

        if self.method[i] == 'ARD':
            self.model = linear.ARDRegression(**params[i])

        if self.method[i] == 'LARS':
            # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            self.model = linear.Lars(**params_temp)

        if self.method[i] == 'SVR':
            self.model = svm.SVR(**params[i])

        if self.method[i] == 'KRR':
            self.model = kernel_ridge.KernelRidge(**params[i])

        if self.method[i] == 'GP':
            self.model = gp.GaussianProcessRegressor(**params[i])

        if self.method[i] == 'GBR':
            self.model = GradientBoostingRegressor(**params[i])


    def fit(self, x, y):
        try:
            self.model.fit(x, y)
            self.goodfit = True
        except Exception as e:
            self.goodfit = False
            print('Model failed to train!')
            traceback.print_stack()
            print(e)

    def predict(self, x, return_std = None):
        if return_std is not None:  #this allows ARD and BRR to give uncertainties along with predictions
            return self.model.predict(np.array(x), return_std=return_std)
        else:
            return self.model.predict(x)

    def calc_Qres_Lev(self, x):
        # calculate spectral residuals
        E = x - np.dot(self.model.x_scores_, self.model.x_loadings_.transpose())
        Q_res = np.dot(E, E.transpose()).diagonal()
        # calculate leverage
        T = self.model.x_scores_
        leverage = np.diag(T @ np.linalg.inv(T.transpose() @ T) @ T.transpose())
        self.leverage = leverage
        self.Q_res = Q_res

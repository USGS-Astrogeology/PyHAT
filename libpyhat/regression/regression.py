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
from sklearn.cross_decomposition.pls_ import PLSRegression
from sklearn.decomposition import PCA, FastICA
from sklearn.ensemble.gradient_boosting import GradientBoostingRegressor
from sklearn.gaussian_process import GaussianProcessRegressor

class regression:
    def __init__(self, method, yrange, params, i=0):  #TODO: yrange doesn't currently do anything. Remove or do something with it!
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

        if self.method[i] == 'LASSO LARS':
            self.model = linear.LassoLars(**params)

        if self.method[i] == 'SVR':
            self.model = svm.SVR(**params[i])

        if self.method[i] == 'KRR':
            self.model = kernel_ridge.KernelRidge(**params[i])

        if self.method[i] == 'GP':
            # get the method for dimensionality reduction and the number of components
            self.reduce_dim = params[i]['reduce_dim']
            self.n_components = params[i]['n_components']
            # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            # Remove parameters not accepted by Gaussian Process
            params_temp.pop('reduce_dim')
            params_temp.pop('n_components')
            self.model = GaussianProcessRegressor(**params_temp)

        if self.method[i] == 'GBR':
            self.model = GradientBoostingRegressor(**params[i])

    def fit(self, x, y, i=0):
        # if gaussian processes are being used, data dimensionality needs to be reduced before fitting
        if self.method[i] == 'GP':
            if self.reduce_dim == 'FastICA':
                print('Reducing dimensionality with ICA')
                do_ica = FastICA(n_components=self.n_components)
                self.do_reduce_dim = do_ica.fit(x)
            if self.reduce_dim == 'PCA':
                print('Reducing dimensionality with PCA')
                do_pca = PCA(n_components=self.n_components)
                self.do_reduce_dim = do_pca.fit(x)

            x = self.do_reduce_dim.transform(x)
        #try:
            print('Training model...')
        try:
            self.model.fit(x, y)
            self.goodfit = True
            #print(self.model)
        except:
            self.goodfit = False
            if self.method[i] == 'GP':
                print('Model failed to train! (For GP this does not always indicate a problem, especially for low numbers of components.)')
                pass
            else:
                print('Model failed to train!')
                traceback.print_stack()

        if self.ransac:
            self.outliers = np.logical_not(self.model.inlier_mask_)
            print(str(np.sum(self.outliers)) + ' outliers removed with RANSAC')



    def predict(self, x, i=0):
        if self.method[i] == 'GP':
            x = self.do_reduce_dim.transform(x)
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

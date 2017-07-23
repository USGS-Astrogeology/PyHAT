# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 11:31:46 2016

@author: rbanderson
"""
import copy

import numpy as np
import sklearn.kernel_ridge as kernel_ridge
import sklearn.linear_model as linear
import sklearn.svm as svm
from sklearn.cross_decomposition.pls_ import PLSRegression
from sklearn.decomposition import PCA, FastICA
from sklearn.gaussian_process import GaussianProcess


class regression:
    def __init__(self, method, yrange, params, i=0, ransacparams={}):
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
                               'Lasso LARS',
                               'SVR',
                               'KRR',
                               ]
        self.method = method
        self.outliers = None
        self.inliers = None
        self.ransac = False

        print(params)
        if self.method[i] == 'PLS':
            self.model = PLSRegression(**params[i])

        if self.method[i] == 'OLS':
            self.model = linear.LinearRegression(**params[i])

        if self.method[i] == 'OMP':
            # check whether to do CV or not
            self.do_cv = params[i]['CV']
            # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            # Remove CV parameter
            params_temp.pop('CV')
            if self.do_cv is False:
                self.model = linear.OrthogonalMatchingPursuit(**params_temp)
            else:
                params_temp.pop('n_nonzero_coefs')
                self.model = linear.OrthogonalMatchingPursuitCV(**params_temp)

        if self.method[i] == 'Lasso':
            # check whether to do CV or not
            self.do_cv = params[i]['CV']
            # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            # Remove CV parameter
            params_temp.pop('CV')

            if self.do_cv is False:
                self.model = linear.Lasso(**params_temp)
            else:
                params_temp.pop('alpha')
                self.model = linear.LassoCV(**params_temp)

        if self.method[i] == 'Elastic Net':
            # check whether to do CV or not
            self.do_cv = params[i]['CV']
            # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            # Remove CV parameter
            params_temp.pop('CV')
            if self.do_cv is False:
                self.model = linear.ElasticNet(**params_temp)
            else:
                params_temp.pop('alpha')
                params_temp['l1_ratio'] = [.1, .5, .7, .9, .95, .99,
                                           1]  # these values recommended by the scikit documentation: http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNetCV.html#sklearn.linear_model.ElasticNetCV
                self.model = linear.ElasticNetCV(**params_temp)

        if self.method[i] == 'Ridge':
            # check whether to do CV or not
            self.do_cv = params[i]['CV']
            # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            # Remove CV parameter
            params_temp.pop('CV')
            if self.do_cv is False:
                self.model = linear.Ridge(**params_temp)
            else:
                self.model = linear.RidgeCV(**params_temp)

        if self.method[i] == 'Bayesian Ridge':
            self.model = linear.BayesianRidge(**params[i])

        if self.method[i] == 'ARD':
            self.model = linear.ARDRegression(**params[i])

        if self.method[i] == 'LARS':
            # check whether to do CV or not
            self.do_cv = params[i]['CV']
            # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            # Remove CV parameter
            params_temp.pop('CV')
            if self.do_cv is False:
                self.model = linear.Lars(**params_temp)
            else:
                self.model = linear.LarsCV(**params_temp)

        if self.method[i] == 'Lasso LARS':
            # check whether to do CV or not
            self.do_cv = params[i]['CV']
            # check whether to do IC or not
            self.do_ic = params[i]['IC']
            # create a temporary set of parameters
            params_temp = copy.copy(params[i])
            # Remove CV and IC parameter
            params_temp.pop('CV')
            params_temp.pop('IC')
            if self.do_cv is False and self.do_ic is False:
                self.model = linear.LassoLars(**params[i])
            if self.do_cv is True and self.do_ic is False:
                self.model = linear.LassoLarsCV(**params[i])
            if self.do_cv is False and self.do_ic is True:
                self.model = linear.LassoLarsIC(**params[i])
            if self.do_cv is True and self.do_ic is True:
                print("Can't use both cross validation AND information criterion to optimize!")

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
            self.model = GaussianProcess(**params_temp)
            # TODO: Why doesn't this if statement work correctly?
            # TODO: This if statement doesn't work because ransacparams is empty
            # < class 'list'>: [{}]
            #        if bool(ransacparams[i]):
            #            print('RANSAC')
            #            self.model=RANSAC(self.model,**ransacparams[i])
            #            self.ransac=True

    def fit(self, x, y, i=0):
        # if gaussian processes are being used, data dimensionality needs to be reduced before fitting
        if self.method[i] == 'GP':
            if self.reduce_dim == 'ICA':
                print('Reducing dimensionality with ICA')
                do_ica = FastICA(n_components=self.n_components)
                self.do_reduce_dim = do_ica.fit(x)
            if self.reduce_dim == 'PCA':
                print('Reducing dimensionality with PCA')
                do_pca = PCA(n_components=self.n_components)
                self.do_reduce_dim = do_pca.fit(x)
            x = self.do_reduce_dim.transform(x)
        try:
            print('Training model...')

            self.model.fit(x, y)

            if self.ransac:
                self.outliers = np.logical_not(self.model.inlier_mask_)
                print(str(np.sum(self.outliers)) + ' outliers removed with RANSAC')

            # if self.method[i]=='PLS' and self.ransac==False:
            #    self.calc_Qres_Lev(x)
            self.goodfit = True
        except:
            print('There was a problem with training the model!')
            self.goodfit = False  # This can happen for GP when dimensionality is reduced too much. Use try/except to handle these cases.

    def predict(self, x, i=0):
        if self.method[i] == 'GP':
            x = self.do_reduce_dim.transform(x)
        print(len(x))
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


def test_PLS():
    regress = regression(method={'PLS'}, yrange={}, params={'n_components': 0, 'scale': False}, ransacparams={})


def test_GP():
    regress = regression(method={'GP'}, yrange={},
                         params={'reduce_dim': 'PCA', 'n_components': 0, 'random_start': 1, 'theta0': 1.0,
                                 'thetaL': 0.1, 'thetaU': 100.0}, ransacparams={})


def test_OLS():
    regress = regression(method={'OLS'}, yrange={}, params={'fit_intercept': True}, ransacparams={})


def test_OMP():
    regress = regression(method={'OMP'}, yrange={}, params={'fit_intercept': True, 'n_nonzero_coefs': 615, 'CV': True},
                         ransacparams={})


def test_Lasso():
    regress = regression(method={'Lasso'}, yrange={},
                         params={'alpha': 1.0, 'fit_intercept': True, 'max_iter': 1000, 'tol': 0.0001,
                                 'positive': False, 'selection': 'random', 'CV': True}, ransacparams={})


def test_Elastic_Net():
    regress = regression(method={'Elastic Net'}, yrange={},
                         params={'alpha': 1.0, 'l1_ratio': 0.5, 'fit_intercept': True, 'normalize': False,
                                 'precompute': 'False', 'max_iter': 1000, 'copy_X': True, 'tol': 0.0001,
                                 'warm_start': False, 'positive': False, 'selection': 'cyclic', 'random_state': 'None'},
                         ransacparams={})


def test_Ridge():
    regress = regression(method={'Ridge'}, yrange={},
                         params={'alpha': 1.0, 'copy_X': True, 'fit_intercept': True, 'max_iter': 'None',
                                 'normalize': False, 'solver': 'auto', 'tol': 0.0, 'random_state': ''}, ransacparams={})


def test_Bayesian_Ridge():
    regress = regression(method={'Bayesian Ridge'}, yrange={},
                         params={'n_iter': 300, 'tol': 0.001, 'alpha_1': 0.001, 'alpha_2': 1e-06, 'lambda_1': 1e-06,
                                 'lambda_2': 1e-06, 'compute_score': False, 'fit_intercept': True, 'normalize': False,
                                 'copy_X': True, 'verbose': False}, ransacparams={})


def test_ARD():
    regress = regression(method={'ARD'}, yrange={},
                         params={'n_iter': 300, 'tol': 0.001, 'alpha_1': 0.001, 'alpha_2': 1e-06, 'lambda_1': 1e-06,
                                 'lambda_2': 1e-06, 'compute_score': False, 'threshold_lambda': 100000,
                                 'fit_intercept': True, 'normalize': False, 'copy_X': True, 'verbose': False},
                         ransacparams={})


def test_LARS():
    regress = regression(method={'LARS'}, yrange={},
                         params={'n_nonzero_coefs': 500, 'fit_intercept': True, 'positive': False, 'verbose': False,
                                 'normalize': False, 'precompute': True, 'copy_X': True, 'eps': 2.220445,
                                 'fit_path': True}, ransacparams={})


def test_Lasso_LARS():
    regress = regression(method={'Lasso LARS'}, yrange={},
                         params={'alpha': 0.0, 'fit_intercept': True, 'positive': False, 'verbose': False,
                                 'normalize': True, 'copy_X': True, 'precompute': 'Auto', 'max_iter': 500,
                                 'eps': 2.220446, 'fit_path': True}, ransacparams={})


def test_SVR():
    regress = regression(method={'SVR'}, yrange={}, params={
        'regression_choosealg_values': ['Choose an algorithm', 'PLS', 'GP', 'OLS', 'OMP', 'Lasso', 'Elastic Net',
                                        'Ridge', 'Bayesian Ridge', 'ARD', 'LARS', 'Lasso LARS', 'SVR', 'KRR',
                                        'More to come...'], 'regression_choosealg_index': 12,
        'regression_choosealg_label': '', 'regression_choosedata_values': ['asdf'], 'regression_choosedata_index': 0,
        'regression_train_choosedata_label': 'Choose data:', 'regression_train_choosex_values': ['comp', 'meta', 'wvl'],
        'regression_train_choosex_index': ['wvl'], 'regression_train_choosex_label': 'X variable:',
        'regression_train_choosey_values': ['SiO2', 'TiO2', 'Al2O3', 'FeOT', 'MnO', 'MgO', 'CaO', 'Na2O', 'K2O'],
        'regression_train_choosey_index': ['SiO2'], 'regression_train_choosey_label': 'Y variable:',
        'yvarmax_label': 'Max:', 'yvarmax_spin': 100.0, 'yvarmin_label': 'Min:', 'yvarmin_spin': 0.0}, ransacparams={})


def test_KRR():
    regress = regression(method={'KRR'}, yrange={},
                         params={'alpha': 0, 'kernel': 'linear', 'gamma': 'None', 'degree': 3.0, 'coef0': 1.0,
                                 'kernel_params': 'None'}, ransacparams={})


test_PLS()
test_GP()
test_OLS()
test_OMP()
test_Lasso()
test_Elastic_Net()
test_Ridge()
test_Bayesian_Ridge()
test_ARD()
test_LARS()
test_Lasso_LARS()
test_SVR()
test_KRR()

# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 11:31:46 2016

@author: rbanderson
"""
import numpy as np
import pysat.spectral.within_range as within_range
from sklearn.cross_decomposition.pls_ import PLSRegression
from sklearn.decomposition import PCA, FastICA
from sklearn.gaussian_process import GaussianProcess
from sklearn.linear_model import RANSACRegressor as RANSAC
from pysat.spectral.meancenter import meancenter
import scipy.optimize as opt
from pysat.plotting import plots 
import copy


class regression:
    def __init__(self,method,params,i=0,ransacparams={}):
        self.method=method 
        self.outliers=None
        self.inliers=None
        self.ransac=False
        
        if self.method[i]=='PLS':
            self.model=PLSRegression(**params[i])
        if self.method[i]=='GP':
            #get the method for dimensionality reduction and the number of components
            self.reduce_dim=params[i]['reduce_dim']
            self.n_components=params[i]['n_components']
            #create a temporary set of parameters            
            params_temp=copy.copy(params[i])
            #Remove parameters not accepted by Gaussian Process
            params_temp.pop('reduce_dim')
            params_temp.pop('n_components')
            self.model=GaussianProcess(**params_temp)
#TODO: Why doesn't this if statement work correctly?            
#        if bool(ransacparams[i]):
#            print('RANSAC')
#            self.model=RANSAC(self.model,**ransacparams[i])
#            self.ransac=True
            
        
    def fit(self,x,y,i=0):
        #if gaussian processes are being used, data dimensionality needs to be reduced before fitting        
        if self.method[i]=='GP':
            if self.reduce_dim=='ICA':
                print('Reducing dimensionality with ICA')
                do_ica=FastICA(n_components=self.n_components)
                self.do_reduce_dim=do_ica.fit(x)
            if self.reduce_dim=='PCA':
                print('Reducing dimensionality with PCA')                
                do_pca=PCA(n_components=self.n_components)
                self.do_reduce_dim=do_pca.fit(x)
            x=self.do_reduce_dim.transform(x)
        try:
            print('Training model...') 
            
            self.model.fit(x,y)
        
            if self.ransac:
                self.outliers=np.logical_not(self.model.inlier_mask_)
                print(str(np.sum(self.outliers))+' outliers removed with RANSAC')
        
            if self.method[i]=='PLS' and self.ransac==False:
                self.calc_Qres_Lev(x)
            self.goodfit=True
        except:
            print('There was a problem with training the model!')
            self.goodfit=False  #This can happen for GP when dimensionality is reduced too much. Use try/except to handle these cases.
            
                
    def predict(self,x,i=0):
        if self.method[i]=='GP':
            x=self.do_reduce_dim.transform(x)
        print(len(x))
        return self.model.predict(x)
        
    def calc_Qres_Lev(self,x):
        #calculate spectral residuals
        E=x-np.dot(self.model.x_scores_,self.model.x_loadings_.transpose())
        Q_res=np.dot(E,E.transpose()).diagonal()
        #calculate leverage                
        T=self.model.x_scores_
        leverage=np.diag(T@np.linalg.inv(T.transpose()@T)@T.transpose())
        self.leverage=leverage
        self.Q_res=Q_res        

        
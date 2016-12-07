# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:16:11 2016
This function is used to run cross validation 
to help choose the optimal number of components. Folds are stratified 
according to a user-specified column

@author: rbanderson
"""
import numpy as np
from sklearn.cross_validation import LeaveOneLabelOut
from sklearn.grid_search import ParameterGrid
from pysat.regression.regression import regression
#from sklearn.linear_model import RANSACRegressor as RANSAC
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

def RMSE(ypred,y):
    return np.sqrt(np.mean((np.squeeze(ypred)-np.squeeze(y))**2))

class cv:
    def __init__(self,params):
        
        print(params)
        self.paramgrid=list(ParameterGrid(params))  #create a grid of parameter permutations

    def do_cv(self,Train,xcols='wvl',ycol=('comp','SiO2'),method='PLS'): #TODO: get RANSAC working with CV
    
        
        cv_iterator=LeaveOneLabelOut(Train[('meta','Folds')])  #create an iterator for cross validation based on the predefined folds
        rmsecv_folds=[]
        rmsec=[]
        rmsecv=[]
        
       
        #loop through the grid of parameters, do cross validation for each permutation
        for i in list(range(len(self.paramgrid))):
            print(self.paramgrid[i])
            #self.modelkey=method+' '+str(self.paramgrid[i])
            #create the estimator object with the current parameters
            
            model=regression([method],[self.paramgrid[i]])
          
            rmsecv_folds_tmp=[]  #Create empty list to hold RMSECV for each fold
            for train,holdout in cv_iterator:  #Iterate through each of the folds in the training set
                
                cvcol=('meta',method+'-CV-'+str(self.paramgrid[i]))#ycol[-1]+'_cv_'+method+'_param'+str(i))  #create the name of the column in which results will be stored
                                
                cv_train=Train.iloc[train]   #extract the data to be used to create the model
                cv_holdout=Train.iloc[holdout]  #extract the data that will be held out of the model
                model.fit(cv_train[xcols],cv_train[ycol])
                if model.goodfit:            
                    y_pred_holdout=model.predict(cv_holdout[xcols])
                else:
                    y_pred_holdout=cv_holdout[ycol]*np.nan
                Train.set_value(Train.index[holdout],cvcol,y_pred_holdout)
                rmsecv_folds_tmp.append(RMSE(y_pred_holdout,cv_holdout[ycol]))
            
            rmsecv_folds.append(rmsecv_folds_tmp)
            rmsecv.append(RMSE(Train[ycol],Train[cvcol]))
              
            model.fit(Train[xcols],Train[ycol])
            if model.goodfit:
                ypred_train=model.predict(Train[xcols])
                pass
            else:
                ypred_train=Train[ycol]*np.nan
            calcol=('meta',method+'-Cal-'+str(self.paramgrid[i]))    
            Train[calcol]=ypred_train
            rmsec.append(RMSE(ypred_train,Train[ycol]))
            
        
        
        output=pd.DataFrame(self.paramgrid)
        output['RMSEC']=rmsec
        output['RMSECV']=rmsecv
        rmsecv_folds=np.array(rmsecv_folds)
        for i in list(range(len(rmsecv_folds[0,:]))):
            label='Fold'+str(i)
            output[label]=rmsecv_folds[:,i]
        return Train,output
        
            
       
               
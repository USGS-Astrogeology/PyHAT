# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:09:29 2016

@author: rbanderson
"""
import pandas as pd
import numpy as np
from pysat.spectral.spectral_data import spectral_data
from pysat.spectral.within_range import within_range
from pysat.spectral.meancenter import meancenter
from pysat.regression.sm import sm
from sklearn.decomposition import PCA, FastICA
from sklearn import linear_model
from sklearn.cross_decomposition.pls_ import PLSRegression
from pysat.plotting import plots
import time
from pysat.regression.cv import cv

import matplotlib.pyplot as plot

print('Read training database')
db=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Sample_Data\full_db_mars_corrected_dopedTiO2_pandas_format.csv"
data=pd.read_csv(db,header=[0,1])

data=spectral_data(data)


print('read unknown data from the combined csv file (much faster)')
unknowndatacsv=r"C:\Users\rbanderson\Documents\Projects\MSL\ChemCam\Lab Data\lab_data_averages_pandas_format.csv"
unknown_data=pd.read_csv(unknowndatacsv,header=[0,1])
unknown_data=spectral_data(unknown_data)

print('Interpolate unknown data onto the same exact wavelengths as the training data')
unknown_data.interp(data.df['wvl'].columns)

print('Mask out unwanted portions of the data')
maskfile=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Input\mask_minors_noise.csv"
data.mask(maskfile)
unknown_data.mask(maskfile)

print('Normalize spectra by specifying the wavelength ranges over which to normalize')
ranges3=[(0,350),(350,470),(470,1000)] #this is equivalent to "norm3"
ranges1=[(0,1000)] #this is equivalent to "norm1"

print('Norm3 data')
data3=data
data3.norm(ranges3)
unknown_data3=unknown_data
unknown_data3.norm(ranges3)

print('norm1 data')
data1=data
data1.norm(ranges1)
unknown_data1=unknown_data
unknown_data1.norm(ranges1)

print('Testing ratio function')
range1=[250,350]
range2=[800,840]
data3.ratio(range1,range2)
data1.ratio(range1,range2)
unknown_data1.ratio(range1,range2)
unknown_data3.ratio(range1,range2)


print('set up for cross validation')
el='SiO2'
nfolds_test=6 #number of folds to divide data into to extract an overall test set
testfold_test=4 #which fold to use as the overall test set

compranges=[[-20,50],[30,70],[60,100],[0,120]] #these are the composition ranges for the submodels
nc=20  #max number of components
outpath=r'C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output'

print('remove a test set to be completely excluded from CV and used to assess the final blended model')
data3.stratified_folds(nfolds=nfolds_test,sortby=('meta',el))
data3_train=data3.rows_match(('meta','Folds'),[testfold_test],invert=True)
data3_test=data3.rows_match(('meta','Folds'),[testfold_test])
 
data1.stratified_folds(nfolds=nfolds_test,sortby=('meta',el))
data1_train=data1.rows_match(('meta','Folds'),[testfold_test],invert=True)
data1_test=data1.rows_match(('meta','Folds'),[testfold_test])
   

ncs=[7,7,5,9] #provide the best # of components for each submodel
traindata=[data3_train.df,data3_train.df,data1_train.df,data3_train.df] #provide training data for each submodel
testdata=[data3_test.df,data3_test.df,data1_test.df,data3_test.df] #provide test data for each submodel
unkdata=[unknown_data3.df,unknown_data3.df,unknown_data1.df,unknown_data3.df] #provide unknown data to be fed to each submodel


labels=['wvl']#,'ratio']
ycol=('meta',el)
method='PLS'

params=[{'n_components':ncs[0],'scale':False},
       {'n_components':ncs[1],'scale':False},
       {'n_components':ncs[2],'scale':False},
       {'n_components':ncs[3],'scale':False}]
         
pls_sm=sm(compranges,method,params)

print('Fitting PLS Submodels (with and without RANSAC)')
x=[]
y=[]
for i in traindata:
    x.append(i[labels])
    y.append(i[ycol])
pls_sm.fit(x,y)


print('Doing PLS Submodel Predictions')
predictions_train=pls_sm.predict(x)
x_test=[]
y_test=[]
for i in testdata:
    x_test.append(i[labels])
    y_test.append(i[ycol])

x_unk=[]
for i in unkdata:
    x_unk.append(i[labels])    
predictions_test=pls_sm.predict(x_test)
predictions_unk=pls_sm.predict(x_unk)

print('Plotting training data predictions')

outpath=r'C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output'
xtitle='Reference wt.%'
ytitle='Predicted wt.%'
plot_title=el
figname='PLS_SM_train_1to1.png'
plots.scatterplot(y,predictions_train,
                  one_to_one=True,lbls=['Low','Mid','High','Full'],figpath=outpath,
                    figname=figname,xtitle=xtitle,ytitle=ytitle,title=plot_title)
    
    


print('Blending PLS submodels')
pass
    






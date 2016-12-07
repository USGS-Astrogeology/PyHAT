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
import warnings

warnings.filterwarnings('ignore')

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

print('Norm3 data')
data3=data
data3.norm(ranges3)
unknown_data3=unknown_data
unknown_data3.norm(ranges3)


print('set up for cross validation')
el='SiO2'
nfolds=6 #number of folds to divide data into to extract an overall test set
testfold=4 #which fold to use as the overall test set

nc=10  #max number of components
outpath=r'C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output'

print('remove a test set to be completely excluded from CV and used to assess the final model')
data3.stratified_folds(nfolds=nfolds,sortby=('meta',el))
data3_train=data3.rows_match(('meta','Folds'),[testfold],invert=True)
data3_test=data3.rows_match(('meta','Folds'),[testfold])
 
print('Do PLS CV')
figfile='PLS_CV_0-100_norm3.png'
params={'n_components':list(range(1,nc+1)),'scale':[False]}
output_pls=cv(data3_train.df,params,xcols='wvl',ycol=('meta',el),method='PLS',ransac=False)

plotx=[output_pls['n_components'],output_pls['n_components']]
ploty=[output_pls['rmsecv'],output_pls['rmsec']]      

alphas=[1.0,1.0]
colors=['r','g']
lbls=['RMSECV','RMSEC']

plots.lineplot(plotx,ploty,lbls=lbls,figpath=outpath,figname=figfile,colors=colors,alphas=alphas,xtitle='# of Components',ytitle='RMSE (wt.%)')

print('Do GP CV - NOTE: This demonstrates looping over several parameters, and GP is slow to begin with, so this will take a while!!')
figfile='GP_CV_0-100_norm3.png'
params={'n_components':list(range(1,nc+1)),'reduce_dim':['ICA'],'regr':['linear'],'theta0':[1],'thetaL':[0.1],'thetaU':[100],'random_start':[1,5,10]}
output=cv(data3_train.df,params,xcols='wvl',ycol=('meta',el),method='GP',ransac=False)

#access the output data frame to create the lists of data to feed to the plotting script
plotx=[output[output['random_start']==1]['n_components'],output[output['random_start']==5]['n_components'],output[output['random_start']==10]['n_components']]
ploty=[output[output['random_start']==1]['rmsecv'],output[output['random_start']==5]['rmsecv'],output[output['random_start']==10]['rmsecv']]      
alphas=[1.0,1.0,1.0]
colors=['r','g','b']
lbls=['RMSECV (rand_start=1)','RMSECV (rand_start=5)','RMSECV (rand_start=10)']

plots.lineplot(plotx,ploty,lbls=lbls,figpath=outpath,figname=figfile,colors=colors,alphas=alphas,xtitle='# of Components',ytitle='RMSE (wt.%)')

pass
    






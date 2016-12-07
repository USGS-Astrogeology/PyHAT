# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:09:29 2016

@author: rbanderson
"""
import pandas as pd
from pysat.spectral.spectral_data import spectral_data
from pysat.plotting import plots
import numpy as np
import warnings
import itertools
import matplotlib.pyplot as plot
import colormaps
import matplotlib
plot.register_cmap(name='viridis',cmap=colormaps.viridis)
    
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

print('Do PCA on data')
data3.pca('wvl',nc=8)
unknown_data3.pca('wvl',load_fit=data3.do_pca)

print('make a pretty plot of PCA results')
elems=['SiO2','TiO2','Al2O3','FeOT','MgO','CaO','Na2O','K2O']
for elem in elems:
    #set up the subplots
    fig=plot.figure()
    fig.set_size_inches(10,4)
    ax1=fig.add_subplot(2,2,(1,3))
    ax2=fig.add_subplot(2,2,2)
    ax3=fig.add_subplot(2,2,4,xlabel='Wavelength (nm)')
    
    #plot the scores
    x=[data3.df[('PCA',1)]]
    y=[data3.df[('PCA',2)]]
    pc1_var=data3.do_pca.explained_variance_ratio_[0]*100
    pc2_var=data3.do_pca.explained_variance_ratio_[1]*100
    
    mappable=ax1.scatter(x,y,c=data3.df[('meta',elem)],cmap='viridis',linewidth=0.2) 
    ax1.set_xlabel('PC1 ('+str(round(pc1_var,1))+r'%)')
    ax1.set_ylabel('PC2 ('+str(round(pc2_var,1))+r'%)')
    
    fig.colorbar(mappable,label=elem,ax=ax1)
    
    #plot the loadings
    x=data3.df['wvl'].columns.values
    pcs=[data3.do_pca.components_[0,:],data3.do_pca.components_[1,:]]
    ax2.plot(x,pcs[0])
    ax3.plot(x,pcs[1])
    
    ax2.set_yticklabels([])
    ax2.set_xticklabels([])
    ax2.set_ylabel('PC1')
    
    ax3.set_yticklabels([])
    ax3.set_ylabel('PC2')
    
    fig.subplots_adjust(hspace=0)
    
    figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output"
    fig.savefig(figpath+r'\PCA_fig'+elem+'.png',dpi=1000)
    

print('Do ICA using JADE algorithm')
#for nc in list(range(7,15)):
nc=11 
data3.ica_jade('wvl',nc=nc,corrcols=[('meta','SiO2'),('meta','TiO2'),('meta','Al2O3'),('meta','FeOT'),('meta','MgO'),('meta','CaO'),('meta','Na2O'),('meta','K2O')])

x=data3.df['wvl'].columns.values
ics=[data3.ica_jade_loadings[0,:].T,data3.ica_jade_loadings[1,:].T]

fig,ax=plot.subplots(nc)
fig.set_size_inches(8,nc)
minorticks=matplotlib.ticker.MultipleLocator(25)

for i,axis in enumerate(ax):
    axis.plot(x,data3.ica_jade_loadings[i,:].T)
    axis.set_yticklabels([])
    axis.xaxis.set_minor_locator(minorticks)
    axis.set_ylabel(data3.ica_jade_ids[i],fontsize=8)
    
    if i<(nc-1):
        axis.set_xticklabels([])
ax[-1].set_xlabel('Wavelength (nm)')
    
fig.subplots_adjust(hspace=0)
plot.savefig(r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output\ICA_loadings_JADE_test_"+str(nc)+".png",dpi=1000)

#O=[data3.df[('ICA_JADE',1)]]
#Ca=[data3.df[('ICA_JADE',2)]]
Na=[data3.df[('ICA_JADE',4)]]
#Mg=[data3.df[('ICA_JADE',4)]]
K=[data3.df[('ICA_JADE',5)]]
#Ca2=[data3.df[('ICA_JADE',6)]]
#Si=[data3.df[('ICA_JADE',7)]]
#Ti=[data3.df[('ICA_JADE',8)]]


print('make a pretty plot of ICA JADE results')
elems=['SiO2','TiO2','Al2O3','FeOT','MgO','CaO','Na2O','K2O']
for elem in elems:
    #set up the subplots
    fig=plot.figure()
    fig.set_size_inches(10,4)
    ax1=fig.add_subplot(2,2,(1,3))
    ax2=fig.add_subplot(2,2,2)
    ax3=fig.add_subplot(2,2,4,xlabel='Wavelength (nm)')
    
    #plot the scores
    
    mappable=ax1.scatter(Na,K,c=data3.df[('meta',elem)],cmap='viridis',linewidth=0.2) 
    ax1.set_xlabel('Na Score')
    ax1.set_ylabel('K score')
    
    fig.colorbar(mappable,label=elem,ax=ax1)
    
    #plot the loadings
    x=data3.df['wvl'].columns.values
    
    ax2.plot(x,data3.ica_jade_loadings[3,:].T)
    ax2.set_yticklabels([])
    ax2.set_xticklabels([])
    ax2.set_ylabel('Na Source')
    
    
    ax3.plot(x,data3.ica_jade_loadings[4,:].T)
    ax3.set_yticklabels([])
    ax3.set_ylabel('K Source')
    
    
    
    fig.subplots_adjust(hspace=0)
    
    figpath=r"C:\Users\rbanderson\Documents\Projects\LIBS PDART\Output"
    fig.savefig(figpath+r'\ICA_fig'+elem+'.png',dpi=1000)


pass
    






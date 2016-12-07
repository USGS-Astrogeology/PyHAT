# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 13:09:21 2016

@author: rbanderson
"""
from matplotlib import pyplot as plot
import numpy as np
import itertools
import pysat.plotting.colormaps as colormaps

def cmaps():
    plot.register_cmap(name='viridis',cmap=colormaps.viridis)
    plot.register_cmap(name='magma',cmap=colormaps.magma)
    plot.register_cmap(name='inferno',cmap=colormaps.inferno)
    plot.register_cmap(name='plasma',cmap=colormaps.plasma)
    

def make_plot(x,y,figpath,figfile=None,xrange=None,yrange=None,xtitle='Reference (wt.%)',ytitle='Prediction (wt.%)',title=None,
                lbl='',one_to_one=False,dpi=1000,
                color=None,annot_mask=None,cmap=None,colortitle='',loadfig=None,masklabel='',marker='o',linestyle='None'):
    if loadfig is not None:
        fig=loadfig
        axes=fig.gca()
    else:
        fig=plot.figure()
            
        axes=fig.gca()
        if title:
            fig.suptitle(title)        
        if xtitle:
            axes.set_xlabel(xtitle)
        if ytitle:
            axes.set_ylabel(ytitle)
        if xrange:
            axes.set_xlim(xrange)
        if yrange:
            axes.set_ylim(yrange)
    
    if one_to_one:
        axes.plot([0, 100], [0, 100],color='k')
    
    if cmap is not None:
        axes.plot(x,y,c=color,cmap=cmap,marker=marker)  
        axes.colorbar(label=colortitle)
    else:
        axes.plot(x,y,color=color,label=lbl,marker=marker,ls=linestyle)
        
        if annot_mask is not None:
            axes.plot(x[annot_mask],y[annot_mask],facecolors='none',linewidth=1.0,label=masklabel,marker=marker)
       
    
    axes.legend(loc='best',fontsize=8,scatterpoints=1,numpoints=1)
    if figpath and figfile:
        fig.savefig(figpath+'/'+figfile,dpi=dpi)
    return fig
    
def pca_ica_plot(data,x_component,y_component,colorvar=None,cmap='viridis',method='PCA',figpath=None,figfile=None):
    cmaps()    
    

    x=[data.df[(method,x_component)]]
    y=[data.df[(method,y_component)]]
    if method=='PCA':
        x_loading=data.do_pca.components_[x_component,:]
        y_loading=data.do_pca.components_[y_component,:]
        
        x_variance=data.do_pca.explained_variance_ratio_[x_component]*100
        y_variance=data.do_pca.explained_variance_ratio_[y_component]*100
        x_label='PC '+str(x_component)+' ('+str(round(x_variance,1))+r'%)'       
        y_label='PC '+str(y_component)+' ('+str(round(y_variance,1))+r'%)'       
        
    if method=='ICA_JADE':
        x_loading=data.ica_jade_loadings[x_component,:].T
        y_loading=data.ica_jade_loadings[y_component,:].T
        x_label='Source '+str(x_component)  
        y_label='Source '+str(y_component)       
        
    #set up the subplots
    fig=plot.figure()
    fig.set_size_inches(10,4)
    ax1=fig.add_subplot(2,2,(1,3))
    ax2=fig.add_subplot(2,2,2)
    ax3=fig.add_subplot(2,2,4,xlabel='Wavelength (nm)')

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    
    if colorvar:
        mappable=ax1.scatter(x,y,c=data.df[colorvar],cmap=cmap,linewidth=0.2) 
        fig.colorbar(mappable,label=colorvar[1],ax=ax1)    
    else:
        mappable=ax1.scatter(x,y,linewidth=0.2) 
    
    #plot the loadings
    wvls=data.df['wvl'].columns.values
    ax2.plot(wvls,x_loading)
    ax3.plot(wvls,y_loading)
    
    ax2.set_yticklabels([])
    ax2.set_xticklabels([])
    ax2.set_ylabel(x_label)
    
    ax3.set_yticklabels([])
    ax3.set_ylabel(y_label)
    
    fig.subplots_adjust(hspace=0)
    
    if figpath and figfile:
        fig.savefig(figpath+'\\'+figfile,dpi=1000)    
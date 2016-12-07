# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 13:07:07 2016

@author: rbanderson
"""

import numpy as np
def meancenter(df,col,previous_mean=None):
    if previous_mean is not None:
        mean_vect=previous_mean
    else:
        mean_vect=df[col].mean(axis=0)
        
    
    #check that the wavelength values match    
    if np.array_equal(mean_vect.index.values,df[col].columns.values):
        df[col]=df[col].sub(mean_vect.values,axis=1)
    else:
        print("Can't mean center! Wavelengths don't match!")    
    
    return df,mean_vect
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 07 12:29:20 2014

@author: rbanderson
"""

import glob
import numpy
import scipy
import baseline_code.ccam_remove_continuum
import ccam_denoise
from scipy.io.idl import readsav
import matplotlib.pyplot as plot
import numpy
import pandas as pd
from pysat.spectral.spectral_data import spectral_data
import mlpy.wavelet

filelist=glob.glob(r"E:\ChemCam\Calibration Data\LANL_testbed\Caltargets\*calib.sav")
filelist2=glob.glob(r"E:\ChemCam\Calibration Data\LANL_testbed\Caltargets\test.sav")
data2=readsav(filelist2[0])
data=readsav(filelist[0])
muv=data['calibspecmuv']
muv_orig=muv
x=data['defuv']#numpy.arange(len(muv))
muv=numpy.array([muv,muv])

muv=pd.DataFrame(muv)
colnames=[]
for i,j in enumerate(x):
    colnames.append(('wvl',x[i]))
muv.columns=pd.MultiIndex.from_tuples(colnames)
muv=spectral_data(muv)
muv2=spectral_data(muv)
muv.remove_baseline(method='ccam',params={'int_flag_':2,'lvmin_':6,'lv_':10})
muv2.remove_baseline(method='wavelet',params=)
#muv_denoise,muv_noise=ccam_denoise.ccam_denoise(muv,sig=3,niter=4)
#plot.figure()
#plot.plot(muv_noise)


#muv_nocont,cont=baseline_code.ccam_remove_continuum.ccam_remove_continuum(x,muv,10,lvmin=6,int_flag=2)
plot.figure(figsize=[11,8])
plot.plot(x,muv.df['wvl'].iloc[0],label='Continuum Removed',linewidth=0.5)
plot.plot(x,muv.df_baseline['wvl'].iloc[0],label='Continuum',linewidth=0.5)
plot.plot(x,muv_orig,label='Original',linewidth=0.5)
plot.plot(x,data2['muv_cont'],label='IDL Continuum',linestyle='--',linewidth=0.5)
plot.legend()
plot.savefig('cont_test.png',dpi=400)
plot.show()

plot.figure(figsize=[11,8])
plot.plot(x,muv.df_baseline['wvl'].iloc[0]-data2['muv_cont'])
plot.savefig('cont_diff.png',dpi=400)
plot.show()

pass


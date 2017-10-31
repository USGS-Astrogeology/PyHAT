# -*- coding: utf-8 -*-
"""
Created on Fri Nov 07 12:29:20 2014

@author: rbanderson
"""

import glob

import baseline_code.ccam_remove_continuum
import matplotlib.pyplot as plot
import numpy
from scipy.io.idl import readsav

filelist = glob.glob(r"E:\ChemCam\Calibration Data\LANL_testbed\Caltargets\*.SAV")
data = readsav(filelist[0])
muv = data['calibspecmuv']
muv_orig = muv
x = numpy.arange(len(muv))

# muv_denoise,muv_noise=ccam_denoise.ccam_denoise(muv,sig=3,niter=4)
# plot.figure()
# plot.plot(muv_noise)

test = baseline_code.ccam_remove_continuum.ccam_remove_continuum(x, muv, 5, 2, 2)
plot.figure()
plot.plot(test)
plot.plot(muv_orig)
cont = muv_orig - test
print(cont[0:20])
plot.plot(cont)
pass

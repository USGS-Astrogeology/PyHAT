"""
Algorithm based on Appendix A of
Starck, J.L., Murtagh, F., 2006. Handbook of Astronomical Data Analysis, 2nd ed. Springer-Verlag.

This is the algorithm used as the basis for ChemCam's denoise and baseline removal as described in
Wiens, R.C., et al., 2013. Pre-flight calibration and initial data processing for the ChemCam laser-induced breakdown
spectroscopy instrument on the Mars Science Laboratory rover. Spectrochimica Acta Part B: Atomic Spectroscopy 82, 1–27.
doi:10.1016/j.sab.2013.02.003

"""

import numpy as np
from scipy import ndimage
import pandas as pd

def wavelet_a_trous(spectrum,n_resolutions):
    kernel = np.array([1, 4, 6, 4, 1],dtype=float) / 16
    w = np.zeros((len(spectrum),n_resolutions+1))
    w[:,0] = spectrum #initialize with the spectrum

    for j in range(n_resolutions):
        #space out the kernel to the appropriate level
        k = np.insert(kernel,[1,2,3,4]*(2**j-1),0)

        wtemp = ndimage.convolve(w[:,j],k,mode='reflect') #convolve the spaced kernel with the current row
        w[:,j] = w[:,j]-wtemp  #set current row to the difference between the current row and convolved version
        w[:,j+1] = wtemp #next row of w is the convolved version
    return w

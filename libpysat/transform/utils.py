# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:11:37 2016

@author: rbanderson
"""
import numpy as np
from pandas import Series
from scipy import signal

import libpysat.transform.baseline_code.watrous as watrous
import numpy
import scipy.signal


def within_range(data, rangevals, col):
    mask = (data[('meta', col)] > rangevals[0]) & (data[('meta', col)] < rangevals[1])
    return data.loc[mask]


def boxcar(y, window_size=3):
    """
    Smooth the input vector using the mean of the neighboring values,
    where neighborhood size is defined by the window.

    Parameters
    ==========
    y : array
        The vector to be smoothed.

    window_size : int
                  An odd integer describing the window size.

    Returns
    =======
     : array
       The smoothed array.

    """
    filt = np.ones(window_size) / window_size
    return Series(np.convolve(y, filt, mode='same'), index=y.index)


def gaussian(y, window_size=3, sigma=2):
    """
    Apply a gaussian filter to smooth the input vector

    Parameters
    ==========
    y :  array
         The input array

    window_size : int
                  An odd integer describing the size of the filter.

    sigma : float
            The numver of standard deviation
    """
    filt = signal.gaussian(window_size, sigma)
    return Series(signal.convolve(y, filt, mode='same'), index=y.index)


# TODO: The common parsing should be a decorator

def band_minima(spectrum, low_endmember=None, high_endmember=None):
    """
    Given two end members, find the minimum observed value inclusively
    between them.

    Parameters
    ==========
    spectrum : pd.series
               Pandas series

    low_endmember : float
                    The low wavelength

    high_endmember : float
                     The high wavelength

    Returns
    =======
    minidx : int
             The wavelength of the minimum value

    minvalue : float
               The observed minimal value
    """
    x = spectrum.index
    y = spectrum

    if not low_endmember:
        low_endmember = x[0]
    if not high_endmember:
        high_endmember = x[-1]

    ny = y[low_endmember:high_endmember]

    minidx = ny.idxmin()
    minvalue = ny.min()

    return minidx, minvalue


def band_center(spectrum, low_endmember=None, high_endmember=None, degree=3):
    x = spectrum.index
    y = spectrum

    if not low_endmember:
        low_endmember = x[0]
    if not high_endmember:
        high_endmember = x[-1]

    ny = y[low_endmember:high_endmember]

    fit = np.polyfit(ny.index, ny, degree)

    center_fit = Series(np.polyval(fit, ny.index), ny.index)
    center = band_minima(center_fit)

    return center, center_fit


def band_area(spectrum, low_endmember=None, high_endmember=None):
    """
    Compute the area under the curve between two endpoints where the
    y-value <= 1.
    """

    x = spectrum.index
    y = spectrum

    if not low_endmember:
        low_endmember = x[0]
    if not high_endmember:
        high_endmember = x[-1]

    ny = y[low_endmember:high_endmember]

    return np.trapz(-ny[ny <= 1.0])


def band_asymmetry(spectrum, low_endmember=None, high_endmember=None):
    """
    Compute the symmetry of an absorption feature as

    (left_area - right_area) / total_area
    """

    x = specturm.index
    y = spectrum

    if not low_endmember:
        low_endmember = x[0]
    if not high_endmember:
        high_endmember = x[-1]

    ny = y[low_endmember:high_endmember]

    center, _ = band_center(ny, low_endmember, high_endmember)

    area_left = band_area(ny[:center], low_endmember, high_endmember)
    area_right = band_area(ny[center:], low_endmember, high_endmember)

    asymmetry = (area_left - area_right) / (area_left + area_right)
    return asymmetry





def get_noise(Data, niter=3):
    """
    ;+
    ; NAME:
    ;     GET_NOISE
    ;
    ; PURPOSE:
    ;    Find the standard deviation of a white gaussian noise in the data.
    ;
    ; CALLING SEQUENCE:
    ;   output=GET_NOISE(Data)
    ;
    ; INPUTS:
    ;   Data -- IDL array
    ;
    ; OPTIONAL INPUT PARAMETERS:
    ;   none
    ;
    ; KEYED INPUTS:
    ;   Niter --scalar: number of iterations for k-sigma clipping
    ;                   default is 3.
    ;
    ; OUTPUTS:
    ;    output
    ;
    ; MODIFICATION HISTORY:
    ;    17-Jan-1996 JL Starck written with template_gen
    ;-  Translated to Python by Ryan Anderson Nov 2014
    """

    vsize = Data.shape
    dim = len(vsize)
    sigma = -1
    if dim == 3:
        nco = vsize[0]
        nli = vsize[1]
        npz = vsize[2]
        indices = range(npz - 2) + 1
        D_cube = numpy.array(nco, nli, npz)
        c1 = -1. / numpy.sqrt(6.)
        c2 = 2. / numpy.sqrt(6.)
        D_cube[:, :, 1:npz - 1] = c1 * (Data[:, :, indices - 1] + Data[:, :, indices + 1]) + c2 * Data[:, :, indices]
        D_cube[:, :, 0] = c2 * (Data[:, :, 0] - Data[:, :, 1])
        D_cube[:, :, npz - 1] = c2 * (Data[:, :, npz - 1] - Data[:, :, npz - 2])
        sigma = sigma_clip(D_cube, niter=niter)
    if dim == 2:
        # ;im_smooth, Data, ima_med, winsize=3, method='median'
        sigma = sigma_clip(Data - ima_med, niter=niter) / 0.969684
    if dim == 1:
        sigma_out, mean = sigma_clip(Data - scipy.signal.medfilt(Data, 3), niter=niter)
        sigma = sigma_out / 0.893421

    return sigma


def sigma_clip(Data, sigma_clip=3.0, niter=2.0):
    """
    ;+
    ; NAME:
    ;       sigma_clip
    ;
    ; PURPOSE:
    ;       return the sigma obtained by k-sigma. Default sigma_clip value is 3.
    ;       if mean is set, the mean (taking into account outsiders) is returned.
    ;
    ; CALLING SEQUENCE:
    ;   output=sigma_clip(Data, sigma_clip=sigma_clip, mean=mean)
    ;
    ; INPUTS:
    ;   Data -- IDL array: data
    ;
    ; OPTIONAL INPUT PARAMETERS:
    ;   none
    ;
    ; KEYED INPUTS:
    ;   sigma_clip -- float : sigma_clip value
    ;
    ; KEYED OUTPUTS:
    ;   mean -- float : mean value
    ;
    ; OUTPUTS:
    ;    output
    ;
    ; EXAMPLE:
    ;    output_sigma = sigma_clip(Image, sigma_clip=2.5)
    ;
    ; MODIFICATION HISTORY:
    ;    25-Jan-1995 JL Starck written with template_gen
    ;-
    """

    output = ''

    # ;------------------------------------------------------------
    # ; function body
    # ;------------------------------------------------------------

    k = sigma_clip
    Ni = niter - 1
    Sig = 0.
    Buff = Data

    m = numpy.sum(Buff) / len(Buff)
    Sig = numpy.std(Buff)
    index = numpy.where(abs(Buff - m) < k * Sig)
    count = len(Buff[index])
    for i in range(1, Ni):
        if count > 0:
            m = numpy.sum(Buff[index]) / len(Buff[index])
            Sig = numpy.std(Buff[index])
            index = numpy.where(abs(Buff - m) < k * Sig)
            count = len(Buff[index])

    output = Sig
    mean = m

    return output, mean


"""
Created on Tue Nov 11 18:29:29 2014
This function is used to denoise a chemcam spectrum.
Based on the function "denoise_spectrum.pro" in IDL
Translated to Python by Ryan Anderson Nov 2014. Modified so that the denoised
spectrum, and the removed noise are returned.
@author: rbanderson
"""


def ccam_denoise(sp_in, sig=3, niter=4):
    s = len(sp_in)
    lv = int(numpy.log(s) / numpy.log(2)) - 1
    ws = watrous.watrous(sp_in, lv)
    ws1 = ws
    for i in range(lv - 2):
        b = get_noise(ws[:, i], niter=niter)
        tmp = ws[:, i]
        ou = numpy.where(abs(tmp) < sig * b)
        nou = len(tmp[ou])
        if nou > 0: tmp[ou] = 0
        ws1[:, i] = tmp
    return numpy.sum(ws1, axis=1), sp_in - numpy.sum(ws1, axis=1)


# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 13:07:07 2016

@author: rbanderson
"""



def meancenter(df, col, previous_mean=None):
    if previous_mean is not None:
        mean_vect = previous_mean
    else:
        mean_vect = df[col].mean(axis=0)

    # check that the wavelength values match
    if np.array_equal(mean_vect.index.values, df[col].columns.values):
        df[col] = df[col].sub(mean_vect.values, axis=1)
    else:
        print("Can't mean center! Wavelengths don't match!")

    return df, mean_vect

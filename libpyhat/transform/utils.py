# -*- coding: utf-8 -*-

import numpy as np
from pandas import Series
from scipy import signal
import numpy


def within_range(data, rangevals, col):
    mask = (data[('meta', col)] > rangevals[0]) & (data[('meta', col)] < rangevals[1])
    return data.loc[mask]

# TODO: The common parsing should be a decorator


def get_noise(data, n_iter = 3):
    """
    Finds the standard deviation of white gaussian noise in the data

    Parameters
    ----------
    data : ndarray
        IDL array of data

    n_iter : int
        Number of iterations to attempt in a sigma clip

    Returns
    -------
    sigma : float
        Standard deviation of white guassian noise
    """

    vsize = data.shape
    dim = len(vsize)
    sigma = -1
    if dim == 3:
        nco = vsize[0]
        nli = vsize[1]
        npz = vsize[2]
        indices = range(npz - 2) + 1
        d_cube = numpy.array(nco, nli, npz)
        c1 = -1. / numpy.sqrt(6.)
        c2 = 2. / numpy.sqrt(6.)
        d_cube[:, :, 1:npz - 1] = c1 * (data[:, :, indices - 1] + data[:, :, indices + 1]) + c2 * data[:, :, indices]
        d_cube[:, :, 0] = c2 * (data[:, :, 0] - Data[:, :, 1])
        d_cube[:, :, npz - 1] = c2 * (data[:, :, npz - 1] - data[:, :, npz - 2])
        sigma = sigma_clip(d_cube, n_iter=n_iter)
    if dim == 2:
        # ;im_smooth, Data, ima_med, winsize=3, method='median'
        sigma = sigma_clip(data - ima_med, n_iter=n_iter) / 0.969684
    if dim == 1:
        sigma_out, mean = sigma_clip(data - signal.medfilt(data, 3), n_iter=n_iter)
        sigma = sigma_out / 0.893421

    return sigma


def sigma_clip(data, sigma_clip=3.0, n_iter=2.0):
    """
    Returns the sigma obtained by k-sigma. If mean is set, the
    mean (taking into account outsiders) is returned.

    Parameters
    ----------
    data : ndarray
        IDL data array

    sigma_clip : float
        Sigma clip value

    n_iter : float
        Number of iterations

    Returns
    -------
    sig : float
        Sigma obtained via k-sigma

    mean : float
        Mean value
    """

    output = ''

    n_iter = n_iter - 1
    sig = 0.
    buff = data

    mean = numpy.sum(buff) / len(buff)
    sig = numpy.std(buff)
    index = numpy.where(abs(buff - m) < sigma_clip * sig)
    count = len(buff[index])

    for i in range(1, Ni):
        if count > 0:
            mean = numpy.sum(buff[index]) / len(buff[index])
            sig = numpy.std(buff[index])
            index = numpy.where(abs(buff - m) < sigma_clip * sig)
            count = len(buff[index])

    return sig, mean


def ccam_denoise(sp_in, sig = 3, n_iter = 4):
    """
    Denoises a chemcam spectrum. Based on the function "denoise_spectrum.pro" in IDL

    Parameters
    ----------
    sp_in : ndarray
        Array of spectrum data

    sig : int
        Unknown

    n_iter : int
        Number of iterations to refine the noise removal

    Returns
    -------
    : float
        The denoised spectrum

    : float
        Removed noise
    """

    s = len(sp_in)
    lv = int(numpy.log(s) / numpy.log(2)) - 1
    ws = watrous.watrous(sp_in, lv)
    ws1 = ws

    for i in range(lv - 2):
        b = get_noise(ws[:, i], n_iter=n_iter)
        tmp = ws[:, i]
        ou = numpy.where(abs(tmp) < sig * b)
        nou = len(tmp[ou])

        if nou > 0:
            tmp[ou] = 0

        ws1[:, i] = tmp

    return numpy.sum(ws1, axis=1), sp_in - numpy.sum(ws1, axis=1)



def meancenter(df, col, previous_mean=None):
    """
    This function subtracts the mean spectrum from a data frame containing multiple spectra.

    Parameters
    ----------
    df : Data frame containing spectra, in the format used by the PyHAT Point Spectra GUI

    col : Top-level column label used to isolate the spectra from metadata (typically 'wvl')

    previous_mean : Iptional vector containing a mean spectrum. This is used to apply the same
                    mean centering to multiple data frames.

    Returns
    -------
    df : mean-centered data frame

    mean_vect : mean spectrum
    """
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

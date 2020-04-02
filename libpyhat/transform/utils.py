# -*- coding: utf-8 -*-
import numpy as np
from pandas import Series
from scipy import signal

import numpy


def within_range(data, rangevals, col):
    mask = (data[('meta', col)] > rangevals[0]) & (data[('meta', col)] < rangevals[1])
    return data.loc[mask]

# TODO: The common parsing should be a decorator



def meancenter(df, col, previous_mean=None):
    """
    This function subtracts the mean spectrum from a data frame containing multiple spectra.
    Parameters
    ----------
    df : Data frame containing spectra, in the format used by the PyHAT Point Spectra GUI
    col : Top-level column label used to isolate the spectra from metadata (typically 'wvl')
    previous_mean : Optional vector containing a mean spectrum. This is used to apply the same
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

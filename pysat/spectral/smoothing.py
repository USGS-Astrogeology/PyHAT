import numpy as np
from pandas import Series
from scipy import signal


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

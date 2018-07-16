import numpy as np
from scipy import signal

def boxcar(y, window_size=3, axis=0, **kwargs):
    """
    Smooth the input vector using the mean of the neighboring values,
    where neighborhood size is defined by the window.

    Parameters
    ==========
    y : array
        The vector to be smoothed.

    window_size : int
                  An odd integer describing the window size.

    axis : int
           Ignored in the 1d case.  In the 2d case, this is the axis
           along which to apply the convolution.
    Returns
    =======
     : array
       The smoothed array.

    """
    if 'mode' not in kwargs.keys():
        kwargs['mode'] = 'same'
    
    filt = np.ones(window_size) / window_size
    if y.ndim == 1:
        return np.convolve(y, filt, **kwargs)
    else:
        return np.apply_along_axis(np.convolve, axis, y, filt, **kwargs)


def gaussian(y, window_size=3, sigma=2, axis=0, **kwargs):
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
    if 'mode' not in kwargs.keys():
        kwargs['mode'] = 'same'
    filt = signal.gaussian(window_size, sigma)
    if y.ndim == 1:
        return np.convolve(y, filt, **kwargs)
    else:
        return np.apply_along_axis(np.convolve, axis, y, filt, **kwargs)
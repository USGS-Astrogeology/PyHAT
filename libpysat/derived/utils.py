import numpy as np

def generic_func(data, wavelengths, kernels={}, func=None, axis=0, **kwargs):
    """
    Using some form of data and a wavelength array. Get the bands associated
    wtih each wavelength in wavelengths, create a subset of bands based off
    of those wavelengths then hand the subset to the function.

    Parameters
    ----------
    data : ndarray
           (x, y, z) 3 dimensional numpy array of a spectra image

    wv_array : iterable
               A list of all possible wavelengths for a given spectral image

    wavelengths : iterable
                  List of wavelengths to use for the function

    Returns
    ----------
    : func
      Returns the result from the given function
    """
    if kernels:
        subset = []
        wvs = data.wavelengths

        for k, v in kernels.items():
            s = sorted(np.abs(wvs-k).argsort()[:v])
            subset.append(np.median(data.iloc[s, :, :], axis=axis))
        if len(subset) == 0:
            subset = subset[0]
    else:
        subset = data.loc[wavelengths, :, :]

    for i in subset:
        i[i == data.no_data_value] = 0

    return func(subset, wavelengths, **kwargs)


def compute_b_a(wavelengths):
    '''
    Given a set of three wavelengths compute there b and a values as per
    the Viviano Beck CRISM Derived Products paper
    (Revised CRISM spectral parameters and summary
    products based on the currently detected
    mineral diversity on Mars)

    Parameters
    ----------
    wavelengths : iterable
        A list of three wavelength values

    Returns
    -------
    b : float
        b value from the paper

    a : float
        a value from the paper
    '''
    wavelengths.sort()
    lambda_s, lambda_c, lambda_l = wavelengths

    b = (lambda_c - lambda_s) / (lambda_l - lambda_s)
    a = 1.0 - b
    return b, a

def compute_slope(x1, x2, y1, y2):
    '''
    Computes slope given two points on a line

    Parameters
    ----------
    x1 : float
        First points x value

    x2 : float
        Second points x value

    y1 : float
        First points y value

    y2 : float
        Second points y value

    Returns
    -------
    : float
        Slope between the two points
    '''

    return (y2 - y1) / (x2 - x1)

def line_fit(slope, x, b):
    '''
    Finds the y value for a given x using a given slope and y intercept

    Parameters
    ----------
    slope : float
        Slope of a line

    x : float
        Point along the x axis of a line

    b : float
        Y intercept of a line

    Returns
    -------
    : float
        Y coordinate corresponding to the given x
    '''
    return (slope * x) + b

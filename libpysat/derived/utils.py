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
        i[i == data.no_data_value] = np.NaN
        
    return func(subset, wavelengths, **kwargs)

def compute_b_a(wavelengths):
    wavelengths.sort()
    lambda_s, lambda_c, lambda_l = wavelengths

    b = (lambda_c - lambda_s) / (lambda_l - lambda_s)
    a = 1.0 - b
    return b, a

def compute_slope(x1, x2, y1, y2):
    return (y2 - y1) / (x2 - x1)

def line_fit(slope, x, b):
    return (slope * x) + b

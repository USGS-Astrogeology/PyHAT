import inspect

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
    return func(subset, **kwargs)

def add_derived_funcs(package):

    derived_funcs = {}

    for module in dir(package):
        if module[0: 2] != "__" and "funcs" not in module:
            new_module = getattr(__import__(package.__name__, fromlist=[module]), module)

            module_funcs = inspect.getmembers(new_module)

            for func in module_funcs:
                if callable(func[1]) and not func[0].endswith('__'):

                    function_name, function = func
                    derived_funcs[function_name] = function

    return derived_funcs

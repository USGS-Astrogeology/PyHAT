import numpy as np

from .import pipe_funcs as pf
from ..utils import generic_func

def bd620(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [419, 619, 749]
    return generic_func(data, wavelengths, func = pf.bd620_func, **kwargs)

def bd1900(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [1408, 1898, 2498]
    return generic_func(data, wavelengths, func = pf.bd1900_func, **kwargs)

def bd2300(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [1578, 2298, 2578]
    return generic_func(data, wavelengths, func = pf.bd2300_func, **kwargs)

def h2o1(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [1578, 2538, 2978]
    return generic_func(data, wavelengths, func = pf.h2o1_func, **kwargs)

def iralbedo(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [1578]
    return generic_func(data, wavelengths, func = pf.iralbedo_func, **kwargs)

def mafic_abs(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [749, 950]
    return generic_func(data, wavelengths, func = pf.mafic_abs_func, **kwargs)

def omh(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [749, 889]
    return generic_func(data, wavelengths, func = pf.omh_func, **kwargs)

def olindex(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [650, 860, 1047, 1230, 1750]
    return generic_func(data, wavelengths, func = pf.olindex_func, **kwargs)

def oneum_min(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    raise NotImplementedError()

def oneum_slope(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [699, 1579]
    return generic_func(data, wavelengths, func = pf.oneum_slope_func, **kwargs)

def reflectance1(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [540]
    return generic_func(data, wavelengths, func = pf.reflectance_func, **kwargs)

def reflectance2(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [749]
    return generic_func(data, wavelengths, func = pf.reflectance_func, **kwargs)

def reflectance3(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [2778]
    return generic_func(data, wavelengths, func = pf.reflectance_func, **kwargs)

def reflectance4(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [1578]
    return generic_func(data, wavelengths, func = pf.reflectance_func, **kwargs)

def thermal_ratio(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [2538, 2978]
    return generic_func(data, wavelengths, func = pf.thermal_ratio_func, **kwargs)

def thermal_slope(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [2538, 2978]
    return generic_func(data, wavelengths, func = pf.thermal_slope_func, **kwargs)

def twoum_ratio(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [1578, 2538]
    return generic_func(data, wavelengths, func = pf.twoum_ratio_func, **kwargs)

def twoum_slope(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [1578, 2538]
    return generic_func(data, wavelengths, func = pf.twoum_slope_func, **kwargs)

def uvvis(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [419, 749]
    return generic_func(data, wavelengths, func = pf.uvvis_func, **kwargs)

def visslope(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [419, 749]
    return generic_func(data, wavelengths, func = pf.visslope_func, **kwargs)

def visuv(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [419, 749]
    return generic_func(data, wavelengths, func = pf.visuv_func, **kwargs)

def visnir(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    wavelengths = [699, 1579]
    return generic_func(data, wavelengths, func = pf.visnir_func, **kwargs)

def calc_bdi_band(data,iteration, initial_band, step, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    iteration : int
                Number of steps to add to the new band calculation

    initial_band : int
                   Initial band to use to calculate the new band

    step : int
           Length between bands to calculate

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    y = initial_band + (step * iteration)
    wv_array = data.wavelengths
    vals = np.abs(data.wavelengths-y)
    minidx = np.argmin(vals) 
    wavelengths = [wv_array[minidx - 3], y, wv_array[minidx + 3]]
    wvlims = [wavelengths[0], y, wavelengths[-1]]
    return generic_func(data, wavelengths, func=pf.bdi_func, wvs=wvlims, **kwargs)

def bdi_generic(data, upper_limit, initial_band, step):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    upper_limit : int
                  Upper limit on the number of wavelengths to be used

    initial_band : int
                   The band to use as a starting point to extract the other
                   0 to upper_limit bands
    step : int
           The step size inbetween the 0 to upper limit bands

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    limit = range(0, upper_limit)
    band_list = [calc_bdi_band(data, i, initial_band, step) for i in limit]
    return 1 - np.sum(band_list, axis = 0)

def bdi1000(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    return bdi_generic(data, 27, 789, 20)

def bdi2000(data, **kwargs):
    """
    Parameters
    ----------
    data : ndarray
           (n,m,p) array

    wv_array : ndarray
               (n,1) array of wavelengths that correspond to the p
               dimension of the data array

    Returns
    -------
     : ndarray
       the processed ndarray
    """
    return bdi_generic(data, 22, 1658, 40)

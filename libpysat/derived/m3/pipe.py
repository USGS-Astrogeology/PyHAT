import numpy as np

from .import pipe_funcs as pf
from ..utils import generic_func

def r750(data, **kwargs):
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

def r950_750(data, **kwargs):
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
    return generic_func(data, wavelengths, func = pf.r950_750_func, **kwargs)

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
    ---
     : ndarray
       the processed ndarray
    """
    wavelengths = [419, 619, 749]
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

def bd950(data, **kwargs):
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
    wavelengths = [749, 949, 1579]
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

def bd1050(data, **kwargs):
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
    wavelengths = [749, 1049, 1579]
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

def bd1250(data, **kwargs):
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
    wavelengths = [749, 1249, 1579]
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

def r1580(data, **kwargs):
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
    wavelengths = [1579]
    return generic_func(data, wavelengths, func = pf.reflectance_func, **kwargs)

def calc_bdi_band(data, iteration, initial_band, step, **kwargs):
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
    return generic_func(data, wavelengths, func=pf.bdi_func, pass_wvs=wvlims, **kwargs)

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
    band_list = [1 - calc_bdi_band(data, i, initial_band, step) for i in limit]

    return np.sum(band_list, axis = 0)

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

# TODO: Implement This
def oneum_fwhm(data, **kwargs):
    raise NotImplementedError()

# TODO: Implement This
def oneum_sym(data, **kwargs):
    raise NotImplementedError()

def bd1umratio(data, **kwargs):
    """
    Name: BD1um Ratio
    Parameter: BD930 / BD990
    Formulation:
    BD930 = 1 - ((R929) / (((R1579 - R699)/(1579 - 699)) * (929-699) + R699))
    BD990 = 1 - ((R989) / (((R1579 - R699)/(1579 - 699)) * (989-699) + R699))
    BDRatio = BD930 / BD990
    Rationale: Possible Ti or impact melt
    Bands: R699, R929, R989, R1579

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
    wavelengths = [699, 929, 989, 1579]
    return generic_func(data, wavelengths, func = pf.bd1umratio_func, **kwargs)

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

def bd2umratio(data, **kwargs):
    """
    Name: BD2um Ratio
    Parameter:2um band depth ratio
    Formulation:
    a = 1 - ((R1898) / (((R2578 - R1578)/(2578 - 1578)) * (1898-1578) + R1578))
    b = 1 - ((R2298) / (((R2578 - R1578)/(2578 - 1578)) * (2298-1578) + R1578))
    BD2um_ratio = a/b
    Rationale: Possible Ti or impact melt
    Bands: R1578, R1898,R2298, R2578

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
    wavelengths = [1578, 1898, 2298, 2578]
    return generic_func(data, wavelengths, func = pf.bd2umratio_func, **kwargs)

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

def bd3000(data, **kwargs):
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
    return generic_func(data, wavelengths, func = pf.bd3000_func, **kwargs)

def r540(data, **kwargs):
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
    wavelengths = [539]
    return generic_func(data, wavelengths, func = pf.reflectance_func, **kwargs)

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

def r2780(data, **kwargs):
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
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

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
    return generic_func(data, wavelengths, func = pf.bd_func, pass_wvs=True, **kwargs)

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

def nbd1400(data, **kwargs):
    """
    Name: NBD1400
    Parameter:1.4um OH Band
    Formulation:
    RC = (R1348 + R1578) / 2
    LC = (R1428 + R1448) / 2
    BB = R1408
    NBD1400 = 1 - 2 * (BB / (RC + LC))
    Rationale: H2O
    Bands: R1348, R1428, R1448, R1578

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
    wavelengths = [1348, 1408, 1428, 1448, 1578]
    return generic_func(data, wavelengths, func = pf.nbd1400_func, **kwargs)

def nbd1480(data, **kwargs):
    """
    Name: NBD1480
    Parameter:1.48um OH Band
    Formulation:
    RC = (R1428 + R1448) / 2
    LC = (R1508 + R1528) / 2
    BB = R1488
    NBD1400 = 1 - 2 * (BB / (RC + LC))
    Rationale: H2O
    Bands: R1428, R1448, R1488, R1508, R1528

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
    wavelengths = [1428, 1448, 1488, 1508, 1528]
    return generic_func(data, wavelengths, func = pf.nbd1480_func, **kwargs)

def nbd2300(data, **kwargs):
    """
    Name: NBD2300
    Parameter: 2.3um OH Band
    Formulation:
    RC = (R2218 + R2258) / 2
    LC = (R2378 + R2418) / 2
    BB = (R2298 + R2338) / 2
    NBD2300 = 1 - 2 * (BB / (RC + LC))
    Rationale: H2O
    Bands: R2218, R2258, R2378, R2418, R2298, R2338

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
    wavelengths = [2218, 2258, 2378, 2418, 2298, 2338]
    return generic_func(data, wavelengths, func = pf.nbd2300_func, **kwargs)

def nbd2700(data, **kwargs):
    """
    Name: HBD2700
    Parameter:2.7um OH Band
    Formulation:
    RC = (R2578 + R2618 + R2658) / 3
    BB = (R2698 + R2738) / 2
    HBD2700 = 1 - (BB / RC)
    Rationale: H2O
    Bands: R2578, R2618, R2658, R2698, R2738

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
    wavelengths = [2578, 2618, 2658, 2698, 2738]
    return generic_func(data, wavelengths, func = pf.nbd2700_func, **kwargs)

def nbd2850(data, **kwargs):
    """
    Name: HBD2850
    Parameter:3um Ice Band
    Formulation:
    RC = (R2538 + R2578 + R2618) / 3
    BB = (R2817 + R2857 + R2897) / 3
    HBD2700 = 1 - (BB / RC)
    Rationale: Ice
    Bands: R2538, R2578, R2618, R2817, R2857, R2897

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
    wavelengths = [2538, 2578, 2618, 2817, 2857, 2897]
    return generic_func(data, wavelengths, func = pf.nbd2850_func, **kwargs)

def hlnd_isfeo(data, **kwargs):
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
    return generic_func(data, wavelengths, func = pf.hlnd_isfeo_func, **kwargs)

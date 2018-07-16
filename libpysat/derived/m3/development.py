from . import development_funcs as dv_funcs

from ..utils import generic_func


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
    return generic_func(data, wavelengths, func = dv_funcs.bd1umratio_func, **kwargs)

def h2o2(data, **kwargs):
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
    return generic_func(data, wavelengths, func = dv_funcs.h2o2_func, **kwargs)

def h2o3(data, **kwargs):
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
    return generic_func(data, wavelengths, func = dv_funcs.h2o3_func, **kwargs)

def h2o4(data, **kwargs):
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
    return generic_func(data, wavelengths, func = dv_funcs.h2o4_func, **kwargs)

def h2o5(data, **kwargs):
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
    return generic_func(data, wavelengths, func = dv_funcs.h2o5_func, **kwargs)

def ice(data, **kwargs):
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
    return generic_func(data, wavelengths, func = dv_funcs.ice_func, **kwargs)

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
    return generic_func(data, wavelengths, func = dv_funcs.bd2umratio_func, **kwargs)

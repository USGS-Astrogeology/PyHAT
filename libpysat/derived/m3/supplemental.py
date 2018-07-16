from . import supplemental_funcs as sp_funcs

from ..utils import generic_func


def curvature(data, **kwargs):
    '''
    Name: Curvature
    Parameter:1 um Band Curvature
    Formulation: (R749 + R1109) / (2* R909)
    Rationale: Tompkins and Pieters
    Bands: 749, R909, R1109

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
    '''
    wavelengths = [749, 909, 1109]
    return generic_func(data, wavelengths, func = sp_funcs.curv_func, **kwargs)

def fe_est(data, **kwargs):
    '''
    Name: FE_est
    Parameter:Iron Estimate
    Formulation:
    y0 = 1.19
    x0 = 0.08
    FE_est = (17.427*(-1*(math.atan(((R949/R749)-y0)/(R749 - x0))))) - 7.565
    Rationale: Iron estimate based on Lucey's Work
    Bands: R749, R949

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
    '''
    wavelengths = [749, 949]
    return generic_func(data, wavelengths, func = sp_funcs.fe_est_func, **kwargs)

def fe_mare_est(data, **kwargs):
    '''
    Name: FE_est_mare
    Parameter:Iron Estimate Mare
    Formulation: -137.97 * ((R749 * 0.9834)+((R949 / R749)*0.1813)) + 57.46
    Rationale: Wilcox et al. JGR (2005), Clementine based
    Bands: R749, R949

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
    '''
    wavelengths = [749, 949]
    return generic_func(data, wavelengths, func = sp_funcs.fe_mare_est_func, **kwargs)

def luceyc_amat(data, **kwargs):
    '''
    Name: Lucey_OMAT
    Parameter:Optimal Maturity - clementine Legacy; Using Adams Constants
    Formulation: (((R749-0.01)**2)+((R949/R749)-1.26)**2)**(1/2)
    Rationale: Based on Lucey et al., JGR (2000)
    Bands: R749, R949

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
    '''
    wavelengths = [749, 949]
    return generic_func(data, wavelengths, func = sp_funcs.luceyc_amat_func, **kwargs)

def luceyc_omat(data, **kwargs):
    '''
    Name: Lucey_OMAT
    Parameter:Optimal Maturity - clementine Legacy; Using Clementine Constants
    Formulation: (((R749-0.08)**2)+((R949/R749)-1.19)**2)**(1/2)
    Rationale: Based on Lucey et al., JGR (2000)
    Bands: R749, R949

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
    '''
    wavelengths = [749, 949]
    return generic_func(data, wavelengths, func = sp_funcs.luceyc_omat_func, **kwargs)

def mare_omat(data, **kwargs):
    '''
    Name: Mare_OMAT
    Parameter:Optical maturity Highlands
    Formulation: (R749 * 0.1813) - ((R949/R749)*0.9834)
    Rationale: Based on Wilcox et al. 2005 - untested
    Bands: R749, R949

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
    '''
    wavelengths = [749, 949]
    return generic_func(data, wavelengths, func = sp_funcs.mare_omat_func, **kwargs)

def tilt(data, **kwargs):
    '''
    Name: Tilt
    Parameter: 1um tilt
    Formulation: R909 - R1009
    Rationale: Tompkins and Pieters

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
    '''

    wavelengths = [930, 1009]
    return generic_func(data, wavelengths,func = sp_funcs.tilt_func,**kwargs)

from . import ip_funcs

def lscc_maturity(data, **kwargs):
    """
    Name: LSCC_Maturity
    Parameter: Optical Maturity revised for hyperspectral data
    Formulation:
    Wk = weighting coefficent from table
    Sum from 1 to 46: Wk * (Rk / Rk_+1) * 10 + C
    Rationale: Based on all Lunar Soil Consortium data
    Bands: R300 - R2600

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

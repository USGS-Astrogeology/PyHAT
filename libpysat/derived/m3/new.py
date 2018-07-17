import numpy as np
from libpysat.derived.m3 import pipe

def mustard(data):
    """
    Name: Visualization from Mustard et al. 2011
    Parameter:1.58um reflectance, 1um integrated band depth, 2um integrated band depth
    Formulation: Red: 1um band depth, Blue: 2um Band Depth, Green: 1.58um reflectance
    Rationale:
    Bands:

    From: JGR Mustard et al. 2011
    Why: Visualization of surface compositional units.

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
    r = pipe.bdi1000(data)
    g = pipe.bdi2000(data)
    b = pipe.r2780(data)

    out = np.empty((r.shape[0], r.shape[1], 3))

    return out

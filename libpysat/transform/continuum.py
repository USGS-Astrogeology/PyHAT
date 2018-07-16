import numpy as np
import numpy.polynomial.polynomial as poly
import pandas as pd
import scipy.stats as ss


def regression(ny, nx, nz=None):
    """
    Compute a continuum using a standard linear regression.

    Parameters
    ----------
    nx : np.ndarray
         A 1d array of the x values (generally wavelength)

    ny : np.ndarray
         A 1d array of the y values (generally the observed)

    nz : np.ndarray
         A 1d array of x values to apply the correction to. This allows
         the domain over which the correction is computed to differ from
         the domain over which the correction is applied.

    Returns
    -------
    y : nd.array
        A 1d continuum correction
    """
    m, b, _, _, _ = ss.linregress(nx, ny)
    if nz is not None:
        y = m * np.asarray(nz) + b
    else:
        y = m * np.asarray(nx) + b
    return y

def linear(ny, nx, nz=None):
    """
    Compute a continuum using a line between two points

    Parameters
    ----------
    data : ndarray
           A 1d array of y (observed) values

    wv_array : ndarray
               array of wavelengths parallel to the wavelengths axis

    axis : int
           The array axis along which the wavelengths exist
    """
    y1 = ny[0]
    y2 = ny[-1]
    wv1 = nx[0]
    wv2 = nx[-1]
    m = (y2 - y1) / (wv2 - wv1)
    b = y1 - (m * wv1)
    if nz is not None:
        y = m*np.asarray(nz) + b
    else:
        y = m * np.asarray(nx) + b
    return y

def polynomial(ny, nx, order=2, nz=None):    
    coeffs = poly.polyfit(nx,ny,order)
    if nz is not None:
        continuum = poly.polyval(nz, coeffs)
    else:
        continuum = poly.polyval(nx, coeffs)
    return continuum


def continuum_correction(data, wv, nodes, correction_nodes=np.array([]),
                         correction=linear, axis=0, adaptive=False,
                         window=3, **kwargs):
    if not correction_nodes:
        correction_nodes = nodes

    correction_idx = []
    for start, stop in zip(correction_nodes, correction_nodes[1:]):
        start = np.where(np.isclose(wv, [start], atol=1))[0][0]
        stop = np.where(np.isclose(wv, [stop], atol=1))[0][0]+1 # +1 as slices are exclusive
        correction_idx.append((start, stop))
    
    # Make a copy of the input data that will house the corrected spectra
    corrected = np.copy(data)
    denom = np.zeros(data.shape)
    
    for i, (start, stop) in enumerate(zip(nodes, nodes[1:])):
        if adaptive:
            start_idx = np.argmax(wv[start-window:start+window+1])
            stop_idx = np.argmin(wv[start-window:start+window+1])
        else:
            # Get the start and stop indices into the wavelength array. These define the correction nodes
            start_idx = np.where(np.isclose(wv, [start], atol=1))[0][0]
            stop_idx = np.where(np.isclose(wv, [stop], atol=1))[0][0]+1 # +1 as slices are exclusive
        # Grab the correction indices.  These define the length of the line to be corrected
        cor_idx = correction_idx[i]
        nodeidx = [slice(None, None)]*len(data.shape)
        nodeidx[axis] = slice(start_idx,stop_idx)
        corridx = [slice(None, None)]*len(data.shape)
        corridx[axis] = slice(cor_idx[0],cor_idx[1])

        
        kwargs['nz'] = wv[cor_idx[0]:cor_idx[1]]
        # Compute an arbitrary correction
        y = np.apply_along_axis(correction, axis, data[nodeidx],
                                wv[start_idx:stop_idx], **kwargs)
        #y = correction(data[tuple(nodeidx)], wv[cor_idx[0]:cor_idx[1]+1], axis=axis, **kwargs)

        # Apply the correction to a copy of the input data and then step to the next subset
        corrected[corridx] = data[corridx] / y
        denom[corridx] = y
    return corrected, denom
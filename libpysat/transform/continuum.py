import numpy as np
import pandas as pd
import scipy.stats as ss


def regression(nx, ny):
    """
    Parameters
    ==========
    specturm : pd.series
               Pandas Series object

    nodes : list
            of nodes to be used for the continuum

    Returns
    =======
    corrected : array
                Continuum corrected array

    continuum : array
                The continuum used to correct the data

    x : array
        The potentially truncated x values
    """

    m, b, r_value, p_value, stderr = ss.linregress(nx, ny)
    c = m * nx + b
    return c


def cubic(spectrum, nodes):
    raise (NotImplemented)


def linear(data, wv_array, axis=0):
    """
    perform linear continuum correction on a ndarray

    parameters
    ----------

    data : ndarray
           The array to continuum correct

    wv_array : ndarray
               array of wavelengths parallel to the wavelengths axis

    axis : int
           The array axis along which the wavelengths exist
    """
    y1 = np.take(data, 0, axis=axis)
    y2 = np.take(data, -1, axis=axis)
    wv1 = wv_array[0]
    wv2 = wv_array[-1]
    m = (y2 - y1) / (wv2 - wv1)
    b = y1 - (m * wv1)

    new_wv_shape = [wv_array.size] + [s for s in m.shape]
    wv_array = np.repeat(wv_array, m.size).reshape(new_wv_shape)

    y = m * wv_array
    y += b

    # reshape the array back to normal
    # TODO: make this less ugly
    for i in range(data.ndim-1):
        y = np.swapaxes(y, i, i+1)
    return y


def regression(data, wv_array):
    m,b,_,_,_ =  ss.linregress(wv_array, data)
    regressed_continuum = m * wv_array + b
    return  data / regressed_continuum


def horgan(data, wv_array, points, window):
    #Define the search windows
    windows = np.empty(len(points), dtype=list)
    for i, point in enumerate(points):
        windows[i] = ((np.where((wv_array > point - window) & (wv_array < point + window))[0]))

    #Get the maximum within the window
    maxima = np.empty(len(points), dtype = int)
    for i, t_window in enumerate(windows):
        maxima[i] = data[t_window.argmax() + t_window[0]]

    x = np.asarray([wv_array[i-1] for i in maxima])
    y = np.asarray([data[i-1] for i in maxima])

    fit = np.polyfit(x,y,2)
    continuum = np.polyval(fit,wv_array)
    continuum_corrected =  data / continuum

    return continuum_corrected


def continuum_correction(data, wv, nodes, correction_nodes=np.array([]), correction=linear, axis=0, **kwargs):
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
        # Get the start and stop indices into the wavelength array. These define the correction nodes
        start_idx = np.where(np.isclose(wv, [start], atol=1))[0][0]
        stop_idx = np.where(np.isclose(wv, [stop], atol=1))[0][0]+1 # +1 as slices are exclusive

        # Grab the correction indices.  These define the length of the line to be corrected
        cor_idx = correction_idx[i]

        nodeidx = [slice(None, None)]*len(data.shape)
        nodeidx[axis] = slice(start_idx,stop_idx)
        corridx = [slice(None, None)]*len(data.shape)
        corridx[axis] = slice(cor_idx[0],cor_idx[1])

        # Compute an arbitrary correction
        y = correction(data[tuple(nodeidx)], wv[cor_idx[0]:cor_idx[1]], axis=axis, **kwargs)

        # Apply the correction to a copy of the input data and then step to the next subset
        vals = data[tuple(corridx)] / y
        corrected[tuple(corridx)] = vals
        denom[tuple(corridx)] = y
    return corrected, denom


correction_methods = {'linear': linear,
                      'regression': regression,
                      'cubic': cubic}

import numpy as np
import pandas as pd
import scipy.stats as ss


def continuum_correct(spectrum, nodes=None, method='linear'):
    """
    Apply a continuum correction to a given spectrum

    Parameters
    ==========
    spectrum : pd.Series
               A pandas series or Spectrum object

    nodes: list
           A list of the nodes between which piecewise continuum
           will be fit

    method : {'linear', 'regresison', 'cubic'}
             The type of regression to be fit, where 'linear' is a piecewise
             linear fit, 'regression' is an Ordinary Least Squares fit, and 
             'cubic' is a 2nd order polynomial fit.

    Returns
    =======
     : pd.Series
       The continuum corrected Spectrum
     
     : pd.Series
       The continuum line
    """

    x = spectrum.index
    y = spectrum
    if not nodes:
        nodes = [x[0], x[-1]]

    return_length = len(y)
    corrected = np.empty(return_length)
    continuum = np.empty(return_length)

    start = 0
    nlist = list(zip(nodes, nodes[1:]))
    for i, n in enumerate(nlist):
        # Define indices into sub-series
        ny = y[n[0]:n[1]]
        nx = ny.index
        if i == 0:
            stop = start + len(y[:n[1]])
            c = correction_methods[method](nx, ny, ex=y[:n[1]].index.values)
            ey = y[:n[1]]
        elif i == len(nlist) - 1:
            stop = start + len(y[n[0]:])
            c = correction_methods[method](nx, ny, ex=y[n[0]:].index.values)
            ey = y[n[0]:]
        else:
            stop = start + len(ny)
            c = correction_methods[method](nx, ny)
            ey = ny

        continuum[start:stop] = c
        corrected[start:stop] = ey / c

        start = stop

    return pd.Series(corrected, index=x), pd.Series(continuum, index=x)


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


def linear(nx, ny, ex=None):
    y1 = ny.iloc[0]
    y2 = ny.iloc[-1]
    wv1 = nx[0]
    wv2 = nx[-1]
    if not isinstance(ex, np.ndarray):
        ex = nx
    m = (y2 - y1) / (wv2 - wv1)
    b = y1 - (m * wv1)

    c = m * ex + b

    return c


def cubic(spectrum, nodes):
    raise (NotImplemented)


correction_methods = {'linear': linear,
                      'regression': regression,
                      'cubic': cubic}

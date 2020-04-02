"""
This baseline removal method is a simple alternative inspired by the wavelet+spline method described for ChemCam.
It divides the spectrum up into windows of a user-specified size, finds the minimum value within each window
that is also a local minimum, and then fits a cubic spline.

"""


from libpyhat.transform.baseline_code.common import Baseline
import libpyhat.transform.baseline_code.wavelet_a_trous as wavelet_a_trous
import numpy as np
import scipy.signal as signal
import scipy.interpolate as interp
import matplotlib.pyplot as plot
import copy
def min_interp(wvl, spectrum, window = 50,kind='cubic'):
    nbands = len(wvl)
    n_windows = np.int(nbands/window)

    all_minima = (signal.argrelextrema(spectrum, np.less)[0])  #find the local minima of the spectrum
    s_minima = []
    for i in range(n_windows):
        ind_window = np.arange(i*window,np.min(((i*window)+window,len(wvl)-1)),1)

        #find the local minima within the current window
        window_minima = all_minima[(all_minima>ind_window[0])&(all_minima<ind_window[-1])]

        #of those, find the one with the minimum value
        current_min = window_minima[np.argmin(spectrum[window_minima])]

        s_minima.append(current_min)

    # add the first and last elements to avoid extrapolation
    s_minima = np.hstack(([0], s_minima, len(spectrum) - 1))

    # remove any duplicates just to be safe
    s_minima = np.unique(s_minima)

    # fit a cubic spline to the points
    if len(s_minima) > 3:
        spline = interp.interp1d(wvl[s_minima], spectrum[s_minima], kind=kind)
        baseline = spline(wvl)
    else:
        # if there aren't enough minima, make the baseline zero
        print('Not enough minima to fit the baseline! Try using a smaller window.')
        baseline = np.zeros_like(wvl)

    return baseline

class minimum_interp(Baseline):
    def __init__(self, window = 50,kind = 'cubic'):
        self.window = window
        self.kind = kind
    def _fit_one(self, x, y):
        return min_interp(x, y, window = self.window, kind = self.kind)
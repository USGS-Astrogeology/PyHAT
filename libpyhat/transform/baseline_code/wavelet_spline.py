"""
This baseline removal method is based on the description of continuum removal in
Wiens, R.C., et al., 2013. Pre-flight calibration and initial data processing for the ChemCam laser-induced breakdown
spectroscopy instrument on the Mars Science Laboratory rover. Spectrochimica Acta Part B: Atomic Spectroscopy 82, 1–27.
doi:10.1016/j.sab.2013.02.003

It uses the wavelet a trous algorithm described in
Starck, J.L., Murtagh, F., 2006. Handbook of Astronomical Data Analysis, 2nd ed. Springer-Verlag.
to decompose the spectrum, then reconstructs the spectrum up to a specified level, finds the local minima in that
smoothed spectrum, then fits a cubic spline to the nearest local minima in the actual spectrum.

Note: this doesn't give identical results to the continuum removal used by ChemCam, but it is pretty close.

"""


from libpyhat.transform.baseline_code.common import Baseline
import libpyhat.transform.baseline_code.wavelet_a_trous as wavelet_a_trous
import numpy as np
import scipy.signal as signal
import scipy.interpolate as interp
import matplotlib.pyplot as plot
import copy
def wave_spline(wvl, spectrum, level=6, levelmin=2):
    s_copy = copy.copy(spectrum)
    # do wavelet transform up to the specified level
    w = wavelet_a_trous.wavelet_a_trous(spectrum, level)

    s_minima = []
    for lev in range(level-1,levelmin-1,-1): #work from high level down to min
        w_minima = (signal.argrelextrema(w[:,lev],np.less)[0]) # find the minima for the current level
        window = 2**lev # search window size corresponds to the size of the kernel at this level
        if len(w_minima) > 0:
            # Find the lowest value in the true spectrum within a window around the wavelet minima
            for i in w_minima:
                ind_window = np.arange(i-window,i+window,1)
                # make sure the window doesn't go beyond the ends of the spectrum
                ind_window = ind_window[ind_window>-1]
                ind_window = ind_window[ind_window<len(spectrum)]
                s_minima.append(ind_window[np.argmin(spectrum[ind_window])])

    # add the first and last elements to avoid extrapolation
    s_minima = np.hstack(([0], s_minima, len(spectrum) - 1))

    # remove any duplicates
    s_minima = np.unique(s_minima)

    # fit a cubic spline to the points
    if len(s_minima) > 3:
        spline = interp.interp1d(wvl[s_minima], spectrum[s_minima], kind='cubic')
        baseline = spline(wvl)
    else:
        # if there aren't enough minima, make the baseline zero
        print('Not enough minima to fit the baseline! Try using a lower Min level.')
        baseline = np.zeros_like(wvl)

    return baseline

class wavelet_spline(Baseline):
    def __init__(self, level = 6, levelmin=2):
        self.levelmin = levelmin
        self.level = level
    def _fit_one(self, x, y):
        return wave_spline(x, y, level = self.level, levelmin = self.levelmin)
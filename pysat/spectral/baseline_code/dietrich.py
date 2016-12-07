import numpy as np
from scipy.ndimage.morphology import binary_erosion
from scipy.signal import convolve

from pysat.spectral.baseline_code.common import iterative_threshold, Baseline


def dietrich_baseline(bands, intensities, half_window=16, num_erosions=10):
  '''
  Fast and precise automatic baseline correction of ... NMR spectra, 1991.
  http://www.sciencedirect.com/science/article/pii/002223649190402F
  http://www.inmr.net/articles/AutomaticBaseline.html
  '''
  # Step 1: moving-window smoothing
  w = half_window*2+1
  window = np.ones(w) / float(w)
  Y = intensities.copy()
  if Y.ndim == 2:
    window = window[None]
  Y[...,half_window:-half_window] = convolve(Y, window, mode='valid')

  # Step 2: Derivative.
  dY = np.diff(Y)**2

  # Step 3: Iterative thresholding.
  is_baseline = np.ones(Y.shape, dtype=bool)
  is_baseline[...,1:] = iterative_threshold(dY)

  # Step 3: Binary erosion, to get rid of peak-tops.
  mask = np.zeros_like(is_baseline)
  mask[...,half_window:-half_window] = True
  s = np.ones(3, dtype=bool)
  if Y.ndim == 2:
    s = s[None]
  is_baseline = binary_erosion(is_baseline, structure=s,
                               iterations=num_erosions, mask=mask)

  # Step 4: Reconstruct baseline via interpolation.
  if Y.ndim == 2:
    return np.row_stack([np.interp(bands, bands[m], y[m])
                         for y, m in zip(intensities, is_baseline)])
  return np.interp(bands, bands[is_baseline], intensities[is_baseline])


class Dietrich(Baseline):
  def __init__(self, half_window=16, num_erosions=10):
    self.half_window_ = half_window
    self.num_erosions_ = num_erosions

  def _fit_many(self, bands, intensities):
    return dietrich_baseline(bands, intensities,
                             half_window=self.half_window_,
                             num_erosions=self.num_erosions_)

  def param_ranges(self):
    return {
        'half_window_': (1, 100, 'integer'),
        'num_erosions_': (1, 20, 'integer')
    }
